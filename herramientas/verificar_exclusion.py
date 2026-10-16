#!/usr/bin/env python3
"""Prueba de exclusión mutua a partir del bag: correlaciona /joint_states con /arm/queue_state.

    python3 exportar_csv.py corrida --salida corrida/
    python3 verificar_exclusion.py corrida/queue_state.csv corrida/joint_states.csv

Idea: un bag de /joint_states NO dice quién publicó cada mensaje. Pero /arm/queue_state dice, a
5 Hz, cuál es el único pedido que se está ejecutando (executing_goal_id). Si a cada mensaje de
/joint_states le asignamos el pedido en ejecución de ese instante, los mensajes de un mismo
pedido tienen que salir en UN solo bloque seguido: si un pedido reaparece después de otro,
dos pedidos movieron el brazo de forma intercalada = violación de exclusión mutua.

Como /arm/queue_state se muestrea cada 0.2 s, un mensaje de /joint_states que cae justo en un
cambio de pedido es ambiguo; se cuenta aparte y no se considera violación.
Entregado como instrumentación: no es lo que evalúa el reto.
"""
import bisect
import csv
import sys


def leer_cola(ruta):
    t, ids = [], []
    with open(ruta, newline='') as f:
        for fila in csv.DictReader(f):
            t.append(int(fila['t_ns']))
            ids.append(fila['executing_goal_id'])
    return t, ids


def leer_joint(ruta):
    with open(ruta, newline='') as f:
        return [int(fila['t_ns']) for fila in csv.DictReader(f)]


def verificar(t_cola, id_cola, t_joint):
    """Devuelve un dict con el resultado de la correlación."""
    orden = []                     # id asignado a cada mensaje no ambiguo, en orden temporal
    ambiguos = sin_pedido = 0
    for t in sorted(t_joint):
        k = bisect.bisect_right(t_cola, t) - 1
        if k < 0 or k + 1 >= len(t_cola):
            ambiguos += 1          # fuera del rango muestreado: no se puede afirmar nada
            continue
        antes, despues = id_cola[k], id_cola[k + 1]
        if antes != despues:
            ambiguos += 1          # cae en un cambio de pedido
        elif antes == '':
            sin_pedido += 1        # se publicó sin ningún pedido en ejecución
        else:
            orden.append(antes)

    bloques = []
    for gid in orden:
        if not bloques or bloques[-1] != gid:
            bloques.append(gid)
    repetidos = sorted({g for g in bloques if bloques.count(g) > 1})
    return {'mensajes': len(t_joint), 'ambiguos': ambiguos, 'sin_pedido': sin_pedido,
            'pedidos': len(set(bloques)), 'bloques': len(bloques), 'repetidos': repetidos}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    r = verificar(*leer_cola(sys.argv[1]), leer_joint(sys.argv[2]))
    print(f"mensajes de /joint_states         : {r['mensajes']}")
    print(f"  asignados a un pedido           : {r['mensajes'] - r['ambiguos'] - r['sin_pedido']}")
    print(f"  en un cambio de pedido (ambiguo): {r['ambiguos']}")
    print(f"  sin pedido en ejecución         : {r['sin_pedido']}")
    print(f"pedidos distintos que movieron    : {r['pedidos']}  (en {r['bloques']} bloques)")
    violaciones = len(r['repetidos']) + r['sin_pedido']
    print(f"VIOLACIONES DE EXCLUSIÓN MUTUA    : {violaciones}")
    if r['repetidos']:
        print('  pedidos que reaparecen después de otro (intercalados):', ', '.join(r['repetidos']))
    if r['sin_pedido']:
        print('  mensajes publicados mientras no había ningún pedido en ejecución')
    print('RESULTADO: ' + ('CUMPLE (cero violaciones)' if violaciones == 0 else 'NO CUMPLE'))
    sys.exit(0 if violaciones == 0 else 1)


if __name__ == '__main__':
    main()
