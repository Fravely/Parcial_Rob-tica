#!/usr/bin/env python3
"""Pregunta 3 · Parte C — ¿dónde se va el tiempo entre la voz y el movimiento?

Lee evidencias/pregunta3/voz_cadena.csv (lo escribe transcriptor_voz) y genera:

  desglose_tiempos.csv / .md   tabla por orden + promedio y mediana, en ms y en %
  desglose_tiempos.png         figura de barras apiladas (si hay matplotlib)
  tabla_cinco_ordenes.md       Parte B: dicho / transcrito / decisión / brazo / correcta

Uso (en el Jetson):
  python3 herramientas/desglose_tiempos.py
  python3 herramientas/desglose_tiempos.py --ordenes 3 4 5 6 7   # solo esas filas (columna n)
  python3 herramientas/desglose_tiempos.py --incluir-texto       # incluye filas en modo texto
  python3 herramientas/desglose_tiempos.py --inicio-movimiento MOVER_PREAGARRE
      # con broker_parte3: el primer movimiento es ir a ESCANEO (antes de la cámara);
      # MOVER_PREAGARRE = el brazo empieza a ir hacia el objeto (incluye percepción, IK y plan)

Etapas: captura del audio, transcripción en la nube, decisión del modelo, envío al
broker, espera en la cola, percepción, cinemática inversa, planificación. Si el
broker no publica estados separados para percepción / IK / planificación, esas tres
se reportan juntas como "salida de cola -> inicio de movimiento" (y así debe decirse
en el informe; no se inventan cifras).
"""
import argparse
import csv
import json
import os
import statistics
import sys

ETAPAS = [
    ('captura_ms', 'Captura del audio'),
    ('transcripcion_ms', 'Transcripción en la nube'),
    ('decision_ms', 'Decisión del modelo (LAYA)'),
    ('envio_a_aceptacion_ms', 'Envío y aceptación en el broker'),
    ('espera_cola_ms', 'Espera en la cola del broker'),
    ('mov_previo_ms', 'Movimiento previo (p. ej. ir a escaneo)'),
    ('percepcion_ms', 'Percepción (cámara)'),
    ('ik_ms', 'Cinemática inversa'),
    ('planificacion_ms', 'Planificación (MoveIt2 / FK de validación)'),
    ('pinza_ms', 'Pinza'),
    ('pre_movimiento_ms', 'Salida de cola → movimiento (sin separar)'),
    ('otros_ms', 'Otros (cómputo local, hilos, logs)'),
]
ESPERA = ('QUEUED', 'EN_COLA', 'ENCOLADO', 'ESPERANDO', 'PENDING', 'PENDIENTE',
          'ACCEPTED', 'ACEPTADO', 'WAITING')
MOV_DEFECTO = ('EXECUTING', 'EJECUT', 'POSTURA', 'IR_', 'MOV', 'ABRIR_PINZA')
COLORES = ['#4C78A8', '#F58518', '#54A24B', '#B279A2', '#E45756', '#9D755D',
           '#72B7B2', '#EECA3B', '#FF9DA6', '#BAB0AC', '#79706E', '#D3D3D3']


def num(v):
    try:
        x = float(v)
        return x if x >= 0 else None
    except (TypeError, ValueError):
        return None


def categoria(estado):
    """UNA categoría por estado del broker (orden de prioridad: sin doble conteo).

    Ej. broker_parte3: VALIDAR_MODELO, PLAN_ESCANEO, ESCANEO:IK_MOVEIT2_SOLO_PLAN,
    ESCANEO:TRAYECTORIA_MOVEIT2_SOLO_PLAN, MOVER_ESCANEO, LOCALIZAR_EN_POSICION_FIJA, ...
    """
    e = estado.upper()
    if any(p in e for p in ('LOCALIZ', 'PERCEP', 'DETECT', 'CAMARA', 'CÁMARA', 'VISION',
                            'VISIÓN', 'COMPROBAR')):
        return 'percepcion_ms'
    if ':IK' in e or e.startswith('IK') or 'CINEMAT' in e:
        return 'ik_ms'
    if any(p in e for p in ('TRAYECT', 'PLAN', 'MOVEIT', 'VALIDAR_MODELO')):
        return 'planificacion_ms'
    if e.startswith(('MOVER', 'MOV', 'EXECUTING', 'EJECUT', 'POSTURA', 'IR_')):
        return 'mov_previo_ms'
    if 'PINZA' in e or 'SOLTAR' in e:
        return 'pinza_ms'
    return 'pre_movimiento_ms'


def analizar_feedback(fb_json, prefijo_mov=None):
    """Devuelve (t_salida_cola, t_inicio_mov, {categoría: ms}) desde el feedback guardado."""
    try:
        fb = [(float(t), str(e), int(p)) for t, e, p in json.loads(fb_json or '[]')]
    except (ValueError, TypeError):
        return None, None, {}
    fuera = [i for i, (_, e, p) in enumerate(fb) if e.upper() not in ESPERA and p <= 0]
    if not fuera:
        return None, None, {}
    i0 = fuera[0]
    if prefijo_mov:
        candidatos = [i for i in fuera if fb[i][1].upper().startswith(prefijo_mov.upper())]
    else:
        candidatos = [i for i in fuera if fb[i][1].upper().startswith(MOV_DEFECTO)]
    if not candidatos:
        return fb[i0][0], None, {}
    i1 = candidatos[0]
    res = {}
    for i in range(i0, i1):
        cat = categoria(fb[i][1])
        res[cat] = res.get(cat, 0.0) + (fb[i + 1][0] - fb[i][0]) * 1000.0
    return fb[i0][0], fb[i1][0], res


def desglosar(fila, prefijo_mov=None):
    d = {k: num(fila.get(k)) for k, _ in ETAPAS[:5]}
    t_sal, t_mov, partes = analizar_feedback(fila.get('feedback_json'), prefijo_mov)
    t_fin = num(fila.get('t_fin_habla'))
    if prefijo_mov:
        total = (t_mov - t_fin) * 1000.0 if (t_mov and t_fin) else None
    else:
        total = num(fila.get('voz_a_movimiento_ms'))
    for k in ('mov_previo_ms', 'percepcion_ms', 'ik_ms', 'planificacion_ms', 'pinza_ms',
              'pre_movimiento_ms'):
        d[k] = partes.get(k)
    if not partes and t_mov is None:  # sin feedback detallado: usar la columna agregada
        d['pre_movimiento_ms'] = num(fila.get('salida_cola_a_movimiento_ms'))
    if total is not None:
        d['otros_ms'] = max(0.0, total - sum(v for v in d.values() if v is not None))
    else:
        d['otros_ms'] = None
    d['total_ms'] = total
    return d


def fmt(v, dec=0):
    return '—' if v is None else f'{v:,.{dec}f}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', default=os.path.expanduser(
        '~/logistica/evidencias/pregunta3/voz_cadena.csv'))
    ap.add_argument('--salida-dir', default=None)
    ap.add_argument('--ordenes', nargs='*', type=int, default=None)
    ap.add_argument('--incluir-texto', action='store_true')
    ap.add_argument('--inicio-movimiento', default=None, metavar='PREFIJO',
                    help='estado del broker que cuenta como "el brazo inicia el movimiento", '
                         'ej. MOVER_PREAGARRE (hacia el objeto). Por defecto: el primer '
                         'movimiento informado (con broker_parte3 es MOVER_ESCANEO).')
    a = ap.parse_args()
    out = a.salida_dir or os.path.dirname(os.path.abspath(a.csv))
    os.makedirs(out, exist_ok=True)

    with open(a.csv, newline='', encoding='utf-8') as f:
        filas = sorted(csv.DictReader(f), key=lambda r: int(r['n']))
    if a.ordenes:
        filas = [r for r in filas if int(r['n']) in a.ordenes]

    # ---------------------------------------------------- Parte B (tabla)
    with open(os.path.join(out, 'tabla_cinco_ordenes.md'), 'w', encoding='utf-8') as f:
        f.write('| # | Lo que se dijo | Lo que transcribió | Decisión del modelo | '
                'Lo que hizo el brazo | ¿Correcta? |\n|---|---|---|---|---|---|\n')
        for r in filas:
            dec = (f"{r['accion']} / {r['objeto']} / {r['color']} · prio {r['prioridad']} · "
                   f"permitido={r['permitido']} ({r['fuente']})") if r['accion'] else '—'
            brazo = r['lo_que_hizo_el_brazo'] or f"[{r['estado_broker']}] {r['mensaje_broker']}"
            f.write(f"| {r['n']} | {r['lo_que_se_dijo'] or '[COMPLETAR]'} | "
                    f"{r['transcripcion']} ({r['modo']}) | {dec} | {brazo} | "
                    f"{r['correcta'] or '[COMPLETAR]'} |\n")

    # ---------------------------------------------------- Parte C (tiempos)
    medibles = [r for r in filas if (a.incluir_texto or r['modo'] == 'voz')
                and desglosar(r, a.inicio_movimiento)['total_ms'] is not None]
    if not medibles:
        print('No hay filas con voz_a_movimiento_ms (¿se envió al broker? ¿modo voz?).')
        print(f'Tabla Parte B escrita en {out}/tabla_cinco_ordenes.md')
        return 1
    des = [(r['n'], desglosar(r, a.inicio_movimiento)) for r in medibles]
    usadas = [(k, n) for k, n in ETAPAS if any(d[k] for _, d in des)]
    # Promedio: es aditivo (la suma de etapas = total), por eso se usa en la figura y el %.
    prom = {k: statistics.mean([d[k] or 0.0 for _, d in des]) for k, _ in usadas}
    med = {k: statistics.median([d[k] or 0.0 for _, d in des]) for k, _ in usadas}
    prom['total_ms'] = statistics.mean([d['total_ms'] for _, d in des])
    med['total_ms'] = statistics.median([d['total_ms'] for _, d in des])

    with open(os.path.join(out, 'desglose_tiempos.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['orden'] + [n for _, n in usadas] + ['Total voz→movimiento'])
        for n_, d in des:
            w.writerow([n_] + [round(d[k] or 0.0, 1) for k, _ in usadas] + [round(d['total_ms'], 1)])
        w.writerow(['promedio'] + [round(prom[k], 1) for k, _ in usadas] + [round(prom['total_ms'], 1)])
        w.writerow(['mediana'] + [round(med[k], 1) for k, _ in usadas] + [round(med['total_ms'], 1)])

    tot = prom['total_ms'] or 1.0
    orden = sorted(usadas, key=lambda kn: -prom[kn[0]])
    with open(os.path.join(out, 'desglose_tiempos.md'), 'w', encoding='utf-8') as f:
        f.write('| Etapa | ' + ' | '.join(f'Orden {n}' for n, _ in des)
                + ' | Promedio (ms) | Mediana (ms) | % del total |\n')
        f.write('|---|' + '---|' * (len(des) + 3) + '\n')
        for k, nombre in usadas:
            f.write(f'| {nombre} | ' + ' | '.join(fmt(d[k]) for _, d in des)
                    + f' | {fmt(prom[k])} | {fmt(med[k])} | {100 * prom[k] / tot:.1f} % |\n')
        f.write('| **Total voz → movimiento** | ' + ' | '.join(fmt(d['total_ms']) for _, d in des)
                + f' | **{fmt(prom["total_ms"])}** | {fmt(med["total_ms"])} | 100 % |\n')

    k0, n0 = orden[0]
    print('\nInicio del movimiento =', a.inicio_movimiento or 'primer movimiento informado')
    print('DESGLOSE (promedio de', len(des), 'órdenes'
          + (' — incluye modo texto' if a.incluir_texto else ' en modo voz') + ')')
    for k, n in orden:
        print(f'  {n:<62} {prom[k]:>9.0f} ms  {100 * prom[k] / tot:5.1f} %')
    print(f'  {"TOTAL (promedio)":<62} {prom["total_ms"]:>9.0f} ms   (mediana {med["total_ms"]:.0f} ms)')
    print(f'\nEtapa dominante: {n0} ({100 * prom[k0] / tot:.1f} % del total).')
    meta = prom['total_ms'] / 2
    print(f'Meta "reducir a la mitad": bajar {meta:,.0f} ms. ¿Alcanza con eliminar UNA etapa?')
    for k, n in orden[:4]:
        print(f'  - si {n} fuera 0 ms -> total {prom["total_ms"] - prom[k]:,.0f} ms '
              f'({"SÍ" if prom[k] >= meta else "no"} alcanza la mitad)')

    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('\n(matplotlib no está instalado: pip3 install matplotlib para la figura)')
        return 0
    etiquetas = [f'Orden {n}' for n, _ in des] + ['Promedio']
    datos = [[(d[k] or 0.0) / 1000 for _, d in des] + [prom[k] / 1000] for k, _ in usadas]
    fig, ax = plt.subplots(figsize=(10, 0.6 * len(etiquetas) + 2.2))
    izq = [0.0] * len(etiquetas)
    for (k, nombre), fila, color in zip(usadas, datos, COLORES):
        ax.barh(etiquetas, fila, left=izq, color=color, label=nombre, edgecolor='white')
        izq = [a + b for a, b in zip(izq, fila)]
    for y, x in enumerate(izq):
        ax.text(x, y, f'  {x:.2f} s', va='center', fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('segundos desde que el operador termina de hablar')
    ax.set_title('Pregunta 3 · ¿Dónde se va el tiempo entre la voz y el movimiento?')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=8, frameon=False)
    ax.spines[['top', 'right']].set_visible(False)
    fig.tight_layout()
    ruta = os.path.join(out, 'desglose_tiempos.png')
    fig.savefig(ruta, dpi=160)
    print(f'\nFigura: {ruta}\nTablas: {out}/desglose_tiempos.md y tabla_cinco_ordenes.md')
    return 0


if __name__ == '__main__':
    sys.exit(main())
