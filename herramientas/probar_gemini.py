#!/usr/bin/env python3
"""Prueba de la clave de Google AI Studio (Pregunta 3) SIN ROS y SIN mover el robot.

    source ~/.clave_gemini            # export GEMINI_API_KEY="..."  (fuera del repositorio)
    python3 herramientas/probar_gemini.py              # internet + clave + modelos
    python3 herramientas/probar_gemini.py prueba.wav   # ademas transcribe ese audio

Nunca imprime la clave: solo su tipo (AQ. = clave nueva de AI Studio, AIza = clave antigua)
y su longitud. Prueba primero la cabecera oficial x-goog-api-key; si Google la rechaza,
prueba ?key= en la URL y dice que parametro usar en el transcriptor.
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = 'https://generativelanguage.googleapis.com/v1beta'
MODELOS = ('gemini-3.5-flash-lite', 'gemini-3.6-flash')


def pedir(url, clave, cuerpo=None, en_url=False, timeout=10.0):
    cab = {'Content-Type': 'application/json'}
    if en_url:
        url += ('&' if '?' in url else '?') + 'key=' + urllib.parse.quote(clave, safe='')
    else:
        cab['x-goog-api-key'] = clave
    datos = json.dumps(cuerpo).encode('utf-8') if cuerpo is not None else None
    req = urllib.request.Request(url, data=datos, headers=cab,
                                 method='POST' if cuerpo is not None else 'GET')
    inicio = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode('utf-8')), (time.perf_counter() - inicio) * 1000
    except urllib.error.HTTPError as exc:
        detalle = exc.read(600).decode('utf-8', 'replace')
        return exc.code, detalle, (time.perf_counter() - inicio) * 1000


def texto_de(resp):
    partes = (resp.get('candidates') or [{}])[0].get('content', {}).get('parts', [])
    return ' '.join(p.get('text', '') for p in partes).strip()


def main():
    clave = (os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY') or '').strip()
    if not clave:
        print('FALTA LA CLAVE. Crea el archivo FUERA del proyecto y cargalo:')
        print('  nano ~/.clave_gemini        # una linea: export GEMINI_API_KEY="TU_CLAVE"')
        print('  chmod 600 ~/.clave_gemini && source ~/.clave_gemini')
        return 2
    tipo = 'AQ. (clave nueva de AI Studio)' if clave.startswith('AQ.') else (
        'AIza (clave antigua)' if clave.startswith('AIza') else 'formato desconocido')
    print(f'Clave encontrada: tipo {tipo}, {len(clave)} caracteres (no se muestra).')
    if clave != clave.strip('"\' '):
        print('AVISO: la clave tiene comillas o espacios pegados; revisa ~/.clave_gemini')

    # 1) Internet + autenticacion: lista de modelos
    metodo_ok = None
    for en_url in (False, True):
        nombre = '?key= en la URL' if en_url else 'cabecera x-goog-api-key'
        try:
            codigo, resp, ms = pedir(BASE + '/models?pageSize=200', clave, en_url=en_url)
        except urllib.error.URLError as exc:
            print(f'SIN INTERNET o Google bloqueado: {exc.reason}')
            print('-> El transcriptor pasara a MODO TEXTO (comportamiento exigido). Revisa la red.')
            return 3
        if codigo == 200:
            metodo_ok = en_url
            nombres = sorted(m['name'].split('/')[-1] for m in resp.get('models', [])
                             if 'generateContent' in m.get('supportedGenerationMethods', []))
            print(f'OK autenticacion con {nombre} ({ms:.0f} ms). Modelos con generateContent: '
                  f'{len(nombres)}')
            for m in MODELOS:
                print(f'   {m:<24} {"DISPONIBLE" if m in nombres else "NO aparece en la lista"}')
            break
        print(f'FALLO con {nombre}: HTTP {codigo} -> {str(resp)[:300]}')
    if metodo_ok is None:
        print('\nLa clave no autentica. Causas tipicas: clave mal copiada o incompleta, clave '
              'bloqueada/borrada en AI Studio, o el error 401 ACCESS_TOKEN_TYPE_UNSUPPORTED de '
              'algunas claves AQ. Genera otra clave en https://aistudio.google.com/apikey y repite.')
        return 4

    # 2) generateContent de texto con el modelo por defecto
    modelo = MODELOS[0]
    cuerpo = {'contents': [{'role': 'user', 'parts': [{'text': 'Responde solo con la palabra OK'}]}],
              'generationConfig': {'temperature': 0.0}}
    codigo, resp, ms = pedir(f'{BASE}/models/{modelo}:generateContent', clave, cuerpo, metodo_ok)
    if codigo == 200:
        print(f'OK generateContent {modelo}: «{texto_de(resp)}» en {ms:.0f} ms')
    else:
        print(f'FALLO generateContent {modelo}: HTTP {codigo} -> {str(resp)[:300]}')
        print('Prueba otro modelo: MODELO_GEMINI=gemini-3.6-flash bash scripts/voz.sh')

    # 3) Opcional: transcribir un .wav igual que el nodo
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        with open(ruta, 'rb') as f:
            audio = base64.b64encode(f.read()).decode('ascii')
        cuerpo = {'contents': [{'role': 'user', 'parts': [
            {'text': 'Transcribe literalmente el audio (idioma: es). Devuelve SOLO el texto dicho.'},
            {'inlineData': {'mimeType': 'audio/wav', 'data': audio}}]}],
            'generationConfig': {'temperature': 0.0}}
        codigo, resp, ms = pedir(f'{BASE}/models/{modelo}:generateContent', clave, cuerpo,
                                 metodo_ok, timeout=20.0)
        if codigo == 200:
            print(f'OK transcripcion de {ruta}: «{texto_de(resp)}» en {ms:.0f} ms')
        else:
            print(f'FALLO transcripcion: HTTP {codigo} -> {str(resp)[:300]}')

    print('\nRESULTADO: usa  bash scripts/voz.sh' +
          ('   (con CLAVE_EN_URL=1 delante, porque solo funciono ?key=)' if metodo_ok else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
