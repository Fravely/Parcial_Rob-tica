"""Pregunta 3 · Parte A — nodo transcriptor_voz.

    voz (micrófono o .wav) -> Google AI Studio (Gemini) -> texto
         -> /interpretar_orden (P1) -> broker /pick_place (P2) -> brazo

    export GEMINI_API_KEY="..."          # la clave SOLO vive en la variable de entorno
    bash scripts/voz.sh        (o: ros2 run laya_ordenes transcriptor_voz --ros-args -p enviar_al_broker:=true)

Requisitos del examen que cubre:
  * La clave se lee de GEMINI_API_KEY (o GOOGLE_API_KEY). Nunca se escribe ni se imprime.
  * Tiene su propio tiempo límite (timeout_transcripcion_s). Si Google no responde a
    tiempo o no hay internet -> pasa a MODO TEXTO POR TECLADO y lo informa
    (log WARN + tópico /voz/estado). El brazo nunca queda esperando.
  * Guarda cada audio .wav junto a su transcripción (.json) y una fila en voz_cadena.csv.
  * Mide las etapas de la Parte C: captura, transcripción, decisión, espera en cola,
    salida de cola -> inicio de movimiento y el total voz -> movimiento.

La transcripción se hace por REST (urllib, sin dependencias extra) con el audio
en línea (inlineData). Así hay UN solo viaje a la nube (no se sube el archivo aparte).
"""
import base64
import csv
import datetime
import json
import math
import os
import signal
import struct
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import wave
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturoTimeout

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String

try:
    from .cadena import ClienteCadena
except ImportError:  # ejecutado como script
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cadena import ClienteCadena


URL_GEMINI = 'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent'

COLUMNAS = [
    'n', 'fecha', 'archivo_audio', 'modo', 'motivo_modo_texto', 'modelo', 'transcripcion',
    'lo_que_se_dijo', 't_fin_habla', 'silencio_final_ms', 'captura_ms', 'transcripcion_ms',
    'decision_ms', 'latencia_http_ms', 'inferencia_ms', 'accion', 'objeto', 'color',
    'prioridad', 'permitido', 'degradada', 'fuente', 'motivo', 'estado_broker',
    'envio_a_aceptacion_ms', 'espera_cola_ms', 'salida_cola_a_movimiento_ms',
    'voz_a_movimiento_ms', 'wait_time_s', 'exec_time_s', 'exito', 'mensaje_broker',
    'physical_verified', 'position_error_mm', 'etapas_broker_json',
    'feedback_json', 'lo_que_hizo_el_brazo', 'resultado_esperado', 'correcta',
]


# ---------------------------------------------------------------- audio
def silencio_final_s(ruta, umbral_min=300.0, ventana_s=0.02):
    """Segundos de silencio al final del WAV (para estimar cuándo terminó de hablar).

    RMS por ventanas de 20 ms; umbral = max(umbral_min, 3 x piso de ruido).
    Devuelve 0.0 si no puede analizarlo.
    """
    try:
        with wave.open(ruta, 'rb') as w:
            if w.getsampwidth() != 2:
                return 0.0
            canales, tasa, n = w.getnchannels(), w.getframerate(), w.getnframes()
            datos = w.readframes(n)
        muestras = struct.unpack('<%dh' % (len(datos) // 2), datos)[::canales]
        paso = max(1, int(tasa * ventana_s))
        rms = []
        for i in range(0, len(muestras) - paso + 1, paso):
            bloque = muestras[i:i + paso]
            rms.append(math.sqrt(sum(x * x for x in bloque) / paso))
        if not rms:
            return 0.0
        piso = sorted(rms)[len(rms) // 5]
        umbral = max(umbral_min, 3.0 * piso)
        ultimo = max((i for i, v in enumerate(rms) if v > umbral), default=-1)
        if ultimo < 0:
            return 0.0
        return (len(rms) - ultimo - 1) * ventana_s
    except (wave.Error, OSError, struct.error):
        return 0.0


def grabar_hasta_enter(ruta, dispositivo=''):
    """Graba con arecord (16 kHz, mono, 16 bit) hasta que el operador presione ENTER.

    Devuelve (t_enter_perf, t_enter_epoca, t_listo_perf).
    """
    cmd = ['arecord', '-q', '-f', 'S16_LE', '-r', '16000', '-c', '1', '-t', 'wav']
    if dispositivo:
        cmd += ['-D', dispositivo]
    cmd.append(ruta)
    proc = subprocess.Popen(cmd)
    print('  🎙️  GRABANDO… presiona ENTER apenas termine de hablar el docente.', flush=True)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass
    t_enter, t_enter_ep = time.perf_counter(), time.time()
    proc.send_signal(signal.SIGINT)  # SIGINT cierra bien la cabecera WAV
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=2)
    if not os.path.exists(ruta) or os.path.getsize(ruta) < 1000:
        raise RuntimeError('arecord no generó audio (revisa: arecord -l y -p dispositivo_alsa)')
    return t_enter, t_enter_ep, time.perf_counter()


# ---------------------------------------------------------- transcripción
def gemini_rest(ruta_wav, modelo, clave, timeout_s, idioma='es', vocabulario=(),
                temperatura=0.0, clave_en_url=False):
    with open(ruta_wav, 'rb') as f:
        audio_b64 = base64.b64encode(f.read()).decode('ascii')
    pista = ', '.join(vocabulario)
    instruccion = (
        f'Transcribe literalmente el audio (idioma: {idioma}). Es una orden corta para un '
        f'brazo robótico. Palabras posibles: {pista}. Devuelve SOLO el texto dicho, '
        f'sin comillas, sin explicaciones. Si no se entiende nada, devuelve una cadena vacía.')
    cuerpo = {
        'contents': [{'role': 'user', 'parts': [
            {'text': instruccion},
            {'inlineData': {'mimeType': 'audio/wav', 'data': audio_b64}},
        ]}],
        'generationConfig': {'temperature': temperatura},
    }
    # Metodo oficial: cabecera x-goog-api-key. La clave nunca se imprime ni se guarda.
    url = URL_GEMINI.format(modelo=modelo)
    cabeceras = {'Content-Type': 'application/json'}
    if clave_en_url:
        url += '?key=' + urllib.parse.quote(clave, safe='')
    else:
        cabeceras['x-goog-api-key'] = clave
    req = urllib.request.Request(url, method='POST', data=json.dumps(cuerpo).encode('utf-8'),
                                 headers=cabeceras)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            resp = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        detalle = exc.read(400).decode('utf-8', 'replace')
        raise RuntimeError(f'HTTP {exc.code} de Google: {detalle}') from None
    partes = (resp.get('candidates') or [{}])[0].get('content', {}).get('parts', [])
    texto = ' '.join(p.get('text', '') for p in partes).strip().strip('"“”').strip()
    return texto


class TranscriptorVoz(Node):
    def __init__(self):
        super().__init__('transcriptor_voz')
        p = self.declare_parameter
        p('fuente_audio', 'microfono')             # 'microfono' o 'archivo'
        p('archivos_audio', [''])                  # rutas .wav si fuente_audio=archivo
        p('dispositivo_alsa', '')                  # ej. 'plughw:2,0' (ver arecord -l)
        p('timeout_transcripcion_s', 6.0)          # tiempo límite PROPIO del nodo
        p('modelo_gemini', 'gemini-3.5-flash-lite')
        p('modelo_gemini_respaldo', 'gemini-3.6-flash')  # solo si el 1º devuelve vacío
        p('temperatura', 0.0)
        p('idioma', 'es')
        p('vocabulario', ['JetCobot', 'recoge', 'deposita', 'cubo', 'rojo', 'azul',
                          'verde', 'amarillo', 'urgente'])
        p('forzar_modo_texto', False)              # demo explícita del modo texto
        p('timeout_decision_s', 5.0)
        p('enviar_al_broker', False)               # SEGURO por defecto
        p('accion_broker', '/logistica/pick_place')
        p('topico_cola', '')                       # '' = <ns de la accion>/arm/queue_state
        # Estado del broker que cuenta como 'el brazo inicia el movimiento' (Parte C).
        # MOVER_AGARRE = el brazo va hacia el cubo, DESPUES de percepcion, IK y plan.
        # Usar 'MOV' para medir hasta el primer movimiento (ir a escaneo).
        p('estado_inicio_movimiento', 'MOVER_AGARRE')
        p('client_id', 'voz')
        p('zona', 'deposito')
        p('timeout_brazo_s', 180.0)
        p('dir_evidencias', os.path.expanduser('~/logistica/evidencias/pregunta3'))
        p('clave_en_url', False)                   # True solo si probar_gemini.sh lo indica

        g = lambda n: self.get_parameter(n).value  # noqa: E731
        self.fuente = str(g('fuente_audio'))
        self.archivos = [a for a in g('archivos_audio') if str(a).strip()]
        self.dispositivo = str(g('dispositivo_alsa'))
        self.timeout_tr = float(g('timeout_transcripcion_s'))
        if not 0.5 <= self.timeout_tr <= 60:
            raise ValueError('timeout_transcripcion_s debe estar entre 0.5 y 60 s')
        self.modelo = str(g('modelo_gemini'))
        self.modelo_resp = str(g('modelo_gemini_respaldo'))
        self.temperatura = float(g('temperatura'))
        self.idioma = str(g('idioma'))
        self.vocab = [str(v) for v in g('vocabulario')]
        self.forzar_texto = bool(g('forzar_modo_texto'))
        self.timeout_dec = float(g('timeout_decision_s'))
        self.enviar = bool(g('enviar_al_broker'))
        self.client_id = str(g('client_id'))
        self.zona = str(g('zona'))
        self.timeout_brazo = float(g('timeout_brazo_s'))
        self.dir = str(g('dir_evidencias'))
        os.makedirs(self.dir, exist_ok=True)
        self.csv = os.path.join(self.dir, 'voz_cadena.csv')

        self.pub_txt = self.create_publisher(String, '/voz/transcripcion', 10)
        self.pub_estado = self.create_publisher(String, '/voz/estado', 10)
        self.lock = threading.RLock()
        self.pendientes = {}  # seg.id -> fila parcial
        self.pool = ThreadPoolExecutor(max_workers=2)
        self.inicio_mov = str(g('estado_inicio_movimiento')).strip() or 'MOV'
        self.clave_en_url = bool(g('clave_en_url'))
        self.cadena = ClienteCadena(self, str(g('accion_broker')), al_actualizar=self._broker,
                                    prefijos_movimiento=(self.inicio_mov,),
                                    topico_cola=str(g('topico_cola')))
        self.n = self._siguiente_n()
        self.get_logger().info(
            f'transcriptor_voz listo · fuente={self.fuente} · modelo={self.modelo} · '
            f'timeout={self.timeout_tr:.1f}s · broker={"SÍ" if self.enviar else "NO (modo seguro)"} '
            f'({g("accion_broker")}, cola {self.cadena.topico_cola}) '
            f'· inicio de movimiento={self.inicio_mov} · evidencias={self.dir}')
        if not self._clave():
            self.get_logger().warn('No hay GEMINI_API_KEY en esta terminal: se usará MODO TEXTO.')

    # ------------------------------------------------------------ util
    @staticmethod
    def _clave():
        return (os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY') or '').strip()

    def _siguiente_n(self):
        if not os.path.exists(self.csv):
            return 1
        with open(self.csv, encoding='utf-8') as f:
            return max(1, sum(1 for _ in f))

    def _estado(self, texto):
        m = String()
        m.data = texto
        self.pub_estado.publish(m)

    # ---------------------------------------------------- transcripción
    def transcribir(self, ruta):
        """Devuelve (texto, modelo, ms). Lanza excepción si no hay texto a tiempo."""
        clave = self._clave()
        if not clave:
            raise RuntimeError('GEMINI_API_KEY no configurada')
        inicio = time.perf_counter()
        limite = inicio + self.timeout_tr
        for modelo in [m for m in (self.modelo, self.modelo_resp) if m]:
            restante = limite - time.perf_counter()
            if restante < 0.3:
                break
            fut = self.pool.submit(gemini_rest, ruta, modelo, clave, restante, self.idioma,
                                   self.vocab, self.temperatura, self.clave_en_url)
            try:
                texto = fut.result(timeout=restante)  # tiempo límite DURO
            except FuturoTimeout:
                raise TimeoutError(f'Google no respondió en {self.timeout_tr:.1f} s') from None
            except urllib.error.URLError as exc:
                raise ConnectionError(f'sin internet / Google inaccesible ({exc.reason})') from None
            if texto:
                return texto, modelo, (time.perf_counter() - inicio) * 1000.0
            self.get_logger().warn(f'{modelo} devolvió transcripción vacía; probando respaldo')
        raise RuntimeError('transcripción vacía')

    def modo_texto(self, motivo):
        aviso = f'MODO TEXTO POR TECLADO — {motivo}'
        self.get_logger().warn(aviso)
        self._estado('MODO_TEXTO: ' + motivo)
        print('\n  ⚠️  ' + aviso)
        try:
            return input('  ⌨️  Escribe la orden > ').strip()
        except (EOFError, KeyboardInterrupt):
            return ''

    # ------------------------------------------------------------ orden
    def procesar(self, ruta_wav=None, t_fin=None, t_fin_ep=None, t_listo=None,
                 texto_manual=None, motivo_manual='', restar_silencio=True):
        fila = {c: '' for c in COLUMNAS}
        fila.update(n=self.n, fecha=datetime.datetime.now().isoformat(timespec='milliseconds'))
        self.n += 1
        silencio = silencio_final_s(ruta_wav) if (ruta_wav and restar_silencio) else 0.0
        if t_fin is not None:
            # Fin real del habla = ENTER - silencio final detectado en el audio.
            t_fin -= silencio
            t_fin_ep -= silencio
            fila['captura_ms'] = round((t_listo - t_fin) * 1000.0, 1)
        fila['silencio_final_ms'] = round(silencio * 1000.0, 1)
        fila['t_fin_habla'] = round(t_fin_ep, 3) if t_fin_ep else ''
        fila['archivo_audio'] = os.path.basename(ruta_wav) if ruta_wav else ''

        texto, modo, motivo_txt, modelo = texto_manual, 'texto', motivo_manual, ''
        if texto is None:
            if self.forzar_texto:
                texto = self.modo_texto('forzado por parámetro (demostración)')
                motivo_txt = 'forzado por parámetro'
            else:
                print('  ☁️  Transcribiendo con Google AI Studio…', flush=True)
                try:
                    texto, modelo, ms = self.transcribir(ruta_wav)
                    fila['transcripcion_ms'] = round(ms, 1)
                    modo = 'voz'
                except Exception as exc:
                    motivo_txt = f'{type(exc).__name__}: {exc}'
                    texto = self.modo_texto(motivo_txt)
        fila.update(modo=modo, motivo_modo_texto=motivo_txt, modelo=modelo, transcripcion=texto)

        if ruta_wav:  # audio + transcripción juntos, para revisar después
            with open(os.path.splitext(ruta_wav)[0] + '.json', 'w', encoding='utf-8') as f:
                json.dump({'audio': os.path.basename(ruta_wav), 'transcripcion': texto,
                           'modo': modo, 'modelo': modelo, 'motivo_modo_texto': motivo_txt,
                           'transcripcion_ms': fila['transcripcion_ms'],
                           'fecha': fila['fecha']}, f, ensure_ascii=False, indent=2)
        m = String()
        m.data = json.dumps({'n': fila['n'], 'texto': texto, 'modo': modo, 'modelo': modelo,
                             'transcripcion_ms': fila['transcripcion_ms']}, ensure_ascii=False)
        self.pub_txt.publish(m)
        print(f'  📝 Texto ({modo}): «{texto}»', flush=True)
        if not texto:
            fila['estado_broker'] = 'sin_orden'
            return self._escribir(fila)

        try:
            dec, ms = self.cadena.interpretar(texto, self.timeout_dec)
        except Exception as exc:
            fila['estado_broker'] = f'sin_decision: {exc}'
            self.get_logger().error(f'Sin decisión de /interpretar_orden: {exc}')
            return self._escribir(fila)
        fila['decision_ms'] = round(ms, 1)
        for k in ('accion', 'objeto', 'color', 'prioridad', 'permitido', 'degradada',
                  'fuente', 'motivo', 'latencia_http_ms', 'inferencia_ms'):
            fila[k] = dec.get(k, '')
        print(f'  🧠 Decisión: {dec["accion"]} / {dec["objeto"]} / {dec["color"]} · '
              f'prioridad={dec["prioridad"]} · permitido={dec["permitido"]} · '
              f'{dec.get("fuente")} · {ms:.0f} ms', flush=True)

        if not dec['permitido']:
            print(f'  ⛔ RECHAZADA antes de encolar: {dec.get("motivo")}', flush=True)
            fila['estado_broker'] = 'rechazada_antes_de_encolar'
            return self._escribir(fila)
        if not self.enviar:
            print('  🔒 MODO SEGURO: no se envió al broker (usa -p enviar_al_broker:=true).')
            fila['estado_broker'] = 'no_enviada_modo_seguro'
            return self._escribir(fila)

        fila['_t_fin_ep'] = t_fin_ep
        with self.lock:  # RLock: los callbacks del executor esperan a que se registre
            seg = self.cadena.enviar_al_broker(dec, self.client_id, texto, self.zona)
            self.pendientes[seg.id] = fila
        if seg.terminado.is_set():  # p. ej. broker apagado: se cierra aquí mismo
            with self.lock:
                fila = self.pendientes.pop(seg.id, None)
            if fila is not None:
                self._finalizar(seg, fila)
        else:
            print('  📦 Enviada al broker; sigue su avance aquí. Puedes dictar la siguiente.')

    def _broker(self, seg):
        """Callback de ClienteCadena (hilo del executor)."""
        print(f'     ↳ broker [{seg.id}] {seg.estado} {seg.mensaje}'
              + (f' (posición {seg.posicion_cola})' if seg.posicion_cola else ''), flush=True)
        if seg.terminado.is_set():
            with self.lock:
                fila = self.pendientes.pop(seg.id, None)
            if fila is not None:
                self._finalizar(seg, fila)

    def _finalizar(self, seg, fila):
        ms = lambda a, b: round((b - a) * 1000.0, 1) if a and b else ''  # noqa: E731
        fila['estado_broker'] = seg.estado
        fila['envio_a_aceptacion_ms'] = ms(seg.t_envio, seg.t_aceptado)
        fila['espera_cola_ms'] = ms(seg.t_aceptado, seg.t_salida_cola)
        if fila['espera_cola_ms'] == '' and seg.wait_time_s is not None and seg.wait_time_s >= 0:
            fila['espera_cola_ms'] = round(seg.wait_time_s * 1000.0, 1)
        fila['salida_cola_a_movimiento_ms'] = ms(seg.t_salida_cola, seg.t_inicio_mov)
        fila['voz_a_movimiento_ms'] = ms(fila.get('_t_fin_ep'), seg.t_inicio_mov)
        fila['wait_time_s'] = seg.wait_time_s if seg.wait_time_s is not None else ''
        fila['exec_time_s'] = seg.exec_time_s if seg.exec_time_s is not None else ''
        fila['exito'] = seg.exito if seg.exito is not None else ''
        fila['mensaje_broker'] = seg.mensaje
        fila['physical_verified'] = '' if seg.physical_verified is None else seg.physical_verified
        fila['position_error_mm'] = '' if seg.position_error_mm is None else seg.position_error_mm
        fila['etapas_broker_json'] = json.dumps(seg.etapas, ensure_ascii=False)
        fila['feedback_json'] = json.dumps(seg.feedback, ensure_ascii=False)
        self._escribir(fila)
        if fila['voz_a_movimiento_ms'] != '':
            print(f'  ⏱️  Orden {fila["n"]}: voz → movimiento = {fila["voz_a_movimiento_ms"]} ms')

    def _escribir(self, fila):
        fila = {k: fila.get(k, '') for k in COLUMNAS}
        with self.lock:
            nuevo = not os.path.exists(self.csv) or os.path.getsize(self.csv) == 0
            with open(self.csv, 'a', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=COLUMNAS)
                if nuevo:
                    w.writeheader()
                w.writerow(fila)

    # ------------------------------------------------------------ bucles
    def bucle_microfono(self):
        print('\n' + '=' * 66 + '\n P3 · VOZ → TEXTO → DECISIÓN → COLA → BRAZO\n' + '=' * 66)
        while rclpy.ok():
            try:
                cmd = input('\n[ENTER]=grabar · t=escribir orden · q=salir > ').strip().lower()
            except (EOFError, KeyboardInterrupt):
                break
            if cmd == 'q':
                break
            if cmd == 't':
                texto = self.modo_texto('elegido por el operador')
                self.procesar(texto_manual=texto, motivo_manual='elegido por el operador')
                continue
            sello = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            ruta = os.path.join(self.dir, f'orden_{self.n:02d}_{sello}.wav')
            try:
                t_fin, t_fin_ep, t_listo = grabar_hasta_enter(ruta, self.dispositivo)
            except (RuntimeError, FileNotFoundError) as exc:
                texto = self.modo_texto(f'micrófono no disponible ({exc})')
                self.procesar(texto_manual=texto, motivo_manual=f'micrófono: {exc}')
                continue
            self.procesar(ruta, t_fin, t_fin_ep, t_listo)

    def bucle_archivos(self):
        for origen in self.archivos:
            print(f'\n▶ Archivo: {origen}')
            if not os.path.isfile(origen):
                self.get_logger().error(f'No existe {origen}')
                continue
            t_fin, t_fin_ep = time.perf_counter(), time.time()
            sello = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            ruta = os.path.join(self.dir, f'orden_{self.n:02d}_{sello}.wav')
            with open(origen, 'rb') as a, open(ruta, 'wb') as b:
                b.write(a.read())
            # En modo archivo no hay "fin de habla" real: captura = copiar el archivo.
            self.procesar(ruta, t_fin, t_fin_ep, time.perf_counter(), restar_silencio=False)

    def esperar_pendientes(self):
        fin = time.time() + self.timeout_brazo
        while time.time() < fin:
            with self.lock:
                if not self.pendientes:
                    return
            time.sleep(0.2)
        self.get_logger().warn('Quedaron pedidos sin resultado; revisa el broker antes de reintentar.')


def main(args=None):
    rclpy.init(args=args)
    nodo = TranscriptorVoz()
    exe = MultiThreadedExecutor(num_threads=4)
    exe.add_node(nodo)
    threading.Thread(target=exe.spin, daemon=True).start()
    try:
        if nodo.fuente == 'archivo':
            nodo.bucle_archivos()
        else:
            nodo.bucle_microfono()
        nodo.esperar_pendientes()
        print(f'\nEvidencias en: {nodo.dir}  (voz_cadena.csv + .wav + .json)')
    except KeyboardInterrupt:
        pass
    finally:
        nodo.pool.shutdown(wait=False, cancel_futures=True)
        exe.shutdown()
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
