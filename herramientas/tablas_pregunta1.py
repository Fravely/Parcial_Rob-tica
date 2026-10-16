#!/usr/bin/env python3
"""Pregunta 1: tablas finales a partir de las dos corridas de evaluar_pregunta1.py.

    python3 herramientas/tablas_pregunta1.py \
        --calma evidencias/pregunta1/calma.csv --carga evidencias/pregunta1/carga.csv

Escribe evidencias/pregunta1/tablas_p1.md (y tablas_p1_latencia.csv, tablas_p1_exactitud.csv):
  1) latencia en calma y bajo carga: mediana y p95 del servicio, del viaje HTTP, del calculo
     que informa el servidor (inferencia) y del resto (red + cola del servidor + serializacion);
  2) exactitud de LAYA y del clasificador por palabras clave sobre el mismo conjunto;
  3) lista de frases que falla cada metodo y en que campo, para el comentario de media pagina.
Solo usa datos medidos; si falta una corrida, la omite.
"""
import argparse
import csv
import math
import os
import statistics

METRICAS = [('latencia_servicio_cliente_ms', 'Servicio /interpretar_orden (cliente ROS 2)'),
            ('latencia_http_ms', 'Ida y vuelta HTTP a LAYA (medido por el nodo)'),
            ('inferencia_ms', 'Cálculo informado por el servidor LAYA'),
            ('resto_http_ms', 'Resto = HTTP − cálculo (red + cola + serialización)')]
CAMPOS = [('accion', 'accion_esperada'), ('objeto', 'objeto_esperado'), ('color', 'color_esperado')]


def leer(ruta):
    if not ruta or not os.path.exists(ruta):
        return None
    with open(ruta, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def numeros(filas, col):
    v = []
    for r in filas:
        try:
            x = float(r[col])
        except (TypeError, ValueError, KeyError):
            continue
        if x >= 0 and math.isfinite(x):
            v.append(x)
    return sorted(v)


def med_p95(v):
    if not v:
        return '—', '—'
    return f'{statistics.median(v):.1f}', f'{v[math.ceil(0.95 * len(v)) - 1]:.1f}'


def b(x):
    return str(x).strip().lower() in ('true', '1', 'si', 'sí')


def errores(r, metodo):
    malos = []
    for campo, esperado in CAMPOS:
        obtenido = r.get(f'{campo}_{metodo}', '')
        if obtenido != r.get(esperado, '').strip().lower():
            malos.append(f'{campo}: {obtenido or "—"} (esperado {r.get(esperado, "")})')
    if b(r.get(f'permitido_{metodo}')) != b(r.get('permitido_esperado')):
        malos.append(f'permitido: {r.get(f"permitido_{metodo}")} (esperado {r.get("permitido_esperado")})')
    return malos


def exactitud(filas):
    laya = [r for r in filas if r.get('fuente') == 'LAYA' and not b(r.get('degradada'))]
    res = {}
    for nombre, grupo, metodo in (('LAYA (respuestas reales, no degradadas)', laya, 'laya'),
                                  ('Palabras clave (respaldo) sobre las 50', filas, 'respaldo'),
                                  ('Servicio completo tal como respondió', filas, 'laya')):
        n = len(grupo)
        ok = sum(not errores(r, metodo) for r in grupo)
        por_campo = {c: sum(r.get(f'{c}_{metodo}', '') == r.get(e, '').strip().lower() for r in grupo)
                     for c, e in CAMPOS}
        perm_ok = sum(b(r.get(f'permitido_{metodo}')) == b(r.get('permitido_esperado')) for r in grupo)
        falsos_perm = sum(b(r.get(f'permitido_{metodo}')) and not b(r.get('permitido_esperado')) for r in grupo)
        falsos_rech = sum(not b(r.get(f'permitido_{metodo}')) and b(r.get('permitido_esperado')) for r in grupo)
        res[nombre] = dict(n=n, ok=ok, pct=(100.0 * ok / n) if n else 0.0, perm_ok=perm_ok,
                           falsos_perm=falsos_perm, falsos_rech=falsos_rech, **por_campo)
    return res, laya


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--calma', default='evidencias/pregunta1/calma.csv')
    ap.add_argument('--carga', default='evidencias/pregunta1/carga.csv')
    ap.add_argument('--salida', default='evidencias/pregunta1/tablas_p1.md')
    a = ap.parse_args()
    corridas = {m: leer(r) for m, r in (('calma', a.calma), ('carga', a.carga))}
    corridas = {m: f for m, f in corridas.items() if f}
    if not corridas:
        raise SystemExit('No hay corridas: ejecuta primero bash scripts/evaluar_p1.sh calma')
    base = os.path.splitext(a.salida)[0]
    L = ['# Pregunta 1 — tablas de resultados', '']

    # 1) latencia
    L += ['## 1. Latencia (ms) en calma y bajo carga', '',
          '| Medida | ' + ' | '.join(f'{m}: mediana | {m}: p95' for m in corridas) + ' |',
          '|---|' + '---|---|' * len(corridas)]
    filas_csv = []
    for col, nombre in METRICAS:
        celdas = []
        for m, filas in corridas.items():
            v = numeros(filas, col)
            md, p = med_p95(v)
            celdas += [md, p]
            filas_csv.append(dict(modo=m, medida=col, n=len(v), mediana_ms=md, p95_ms=p))
        L.append(f'| {nombre} | ' + ' | '.join(celdas) + ' |')
    L.append('')
    for m, filas in corridas.items():
        reales = sum(r.get('fuente') == 'LAYA' and not b(r.get('degradada')) for r in filas)
        degradadas = [r for r in filas if b(r.get('degradada'))]
        timeouts = sum('Timeout' in r.get('motivo', '') for r in degradadas)
        confianza = sum('confianza' in r.get('motivo', '') for r in degradadas)
        sin = sum(r.get('estado_solicitud') != 'ok' for r in filas)
        L.append(f'- **{m}**: {len(filas)} frases · LAYA real {reales} · degradadas {len(degradadas)} '
                 f'(timeout {timeouts}, baja confianza {confianza}, otras {len(degradadas) - timeouts - confianza}) '
                 f'· sin respuesta del servicio {sin}')
    L.append('')
    with open(base + '_latencia.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['modo', 'medida', 'n', 'mediana_ms', 'p95_ms'])
        w.writeheader(); w.writerows(filas_csv)

    # 2) exactitud (sobre la corrida en calma si existe)
    m_ex = 'calma' if 'calma' in corridas else next(iter(corridas))
    res, laya = exactitud(corridas[m_ex])
    L += [f'## 2. Exactitud (corrida en {m_ex}; acierto = acción, objeto, color y permitido correctos)', '',
          '| Método | n | Aciertos | Exactitud | Acción | Objeto | Color | Permitido | Falsos permitidos | Falsos rechazos |',
          '|---|---|---|---|---|---|---|---|---|---|']
    filas_ex = []
    for nombre, x in res.items():
        L.append(f'| {nombre} | {x["n"]} | {x["ok"]} | {x["pct"]:.1f} % | {x["accion"]} | {x["objeto"]} | '
                 f'{x["color"]} | {x["perm_ok"]} | {x["falsos_perm"]} | {x["falsos_rech"]} |')
        filas_ex.append(dict(metodo=nombre, **{k: (round(v, 1) if isinstance(v, float) else v) for k, v in x.items()}))
    L += ['', 'La prioridad no entra en la exactitud: LAYA (score × 50) y las palabras clave (20/80/180) '
          'usan escalas distintas.', '']
    with open(base + '_exactitud.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(filas_ex[0]))
        w.writeheader(); w.writerows(filas_ex)

    # 3) frases que falla cada metodo
    L += ['## 3. Frases que falla cada método (para el comentario)', '', '### LAYA (no degradadas)', '']
    L += [f'- «{r["frase"]}» → ' + '; '.join(errores(r, 'laya')) for r in laya if errores(r, 'laya')] or ['- ninguna']
    L += ['', '### LAYA degradada (el servicio usó el respaldo)', '']
    L += [f'- «{r["frase"]}» → {r.get("motivo", "")[:120]}' for r in corridas[m_ex] if b(r.get('degradada'))] or ['- ninguna']
    L += ['', '### Palabras clave', '']
    L += [f'- «{r["frase"]}» → ' + '; '.join(errores(r, 'respaldo')) for r in corridas[m_ex]
          if errores(r, 'respaldo')] or ['- ninguna']
    with open(a.salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))
    print(f'\nEscrito: {a.salida}, {base}_latencia.csv, {base}_exactitud.csv')


if __name__ == '__main__':
    main()
