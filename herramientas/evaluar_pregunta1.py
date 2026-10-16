#!/usr/bin/env python3
"""Prueba ROS 2 de 50 frases con LAYA remoto y respaldo local (Pregunta 1).

Entrada CSV: frase,accion_esperada,objeto_esperado,color_esperado,prioridad_esperada,permitido_esperado
El valor exacto de prioridad se registra, pero no se incluye en la exactitud de
4 campos porque los métodos usan escalas diferentes; documentar criterio si el
docente requiere prioridad dentro del indicador.

El archivo de resultados y las tablas se crean con datos medidos, nunca simulados.
"""
import argparse
import csv
import math
import os
import statistics
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from laya_ordenes_interfaces.srv import InterpretarOrden
from laya_ordenes.logic import clasificar_respaldo


ESPERADO = ['frase', 'accion_esperada', 'objeto_esperado', 'color_esperado',
            'prioridad_esperada', 'permitido_esperado']
SALIDA = ESPERADO + [
    'modo', 'estado_solicitud', 'error', 'accion_laya', 'objeto_laya', 'color_laya',
    'prioridad_laya', 'permitido_laya', 'fuente', 'degradada',
    'accion_respaldo', 'objeto_respaldo', 'color_respaldo',
    'prioridad_respaldo', 'permitido_respaldo',
    'acierto_laya_4campos', 'acierto_respaldo_4campos',
    'latencia_servicio_cliente_ms', 'latencia_http_ms', 'inferencia_ms',
    'resto_http_ms', 'motivo',
]


def bool_esperado(value):
    val = value.strip().lower()
    if val in ('true', '1', 'si', 'sí', 'yes'):
        return True
    if val in ('false', '0', 'no'):
        return False
    return None


def coincidencia(decision, row):
    campos = ['accion_esperada', 'objeto_esperado', 'color_esperado']
    if any(not row.get(k, '').strip() for k in campos):
        return None
    permitir = bool_esperado(row.get('permitido_esperado', ''))
    if permitir is None:
        return None
    return (decision['accion'] == row['accion_esperada'].strip().lower()
            and decision['objeto'] == row['objeto_esperado'].strip().lower()
            and decision['color'] == row['color_esperado'].strip().lower()
            and bool(decision['permitido']) == permitir)


def mediana_p95(vs):
    # percentil 95 por rango más próximo: índice ceil(0.95*N)-1.
    # Evita el índice desfasado de int((N-1)*.95).
    if not vs:
        return '', ''
    ordenados = sorted(vs)
    return round(statistics.median(ordenados), 3), round(ordenados[math.ceil(0.95 * len(ordenados))-1], 3)


def main():
    p = argparse.ArgumentParser(description='Evaluación de 50 frases para /interpretar_orden')
    p.add_argument('--entrada', required=True)
    p.add_argument('--salida', required=True)
    p.add_argument('--modo', required=True, choices=['calma', 'carga'])
    p.add_argument('--timeout', type=float, default=10., help='Espera del cliente ROS (segundos)')
    p.add_argument('--objetos', nargs='+', default=['cubo', 'botella', 'pelota', 'caja'])
    p.add_argument('--colores', nargs='+', default=['rojo', 'azul', 'verde', 'amarillo'])
    args = p.parse_args()
    if args.timeout <= 0:
        p.error('--timeout debe ser positivo')

    with open(args.entrada, newline='', encoding='utf-8-sig') as file:
        primera = file.readline()
        file.seek(0)
        # Excel en espanol guarda los CSV con punto y coma.
        separador = ';' if primera.count(';') > primera.count(',') else ','
        reader = csv.DictReader(file, delimiter=separador)
        if not reader.fieldnames or not set(ESPERADO).issubset(reader.fieldnames):
            raise SystemExit('CSV incorrecto; columnas requeridas: ' + ','.join(ESPERADO))
        frases = list(reader)
    if len(frases) != 50:
        raise SystemExit(f'Deben ser 50 frases REALES del docente; el CSV contiene {len(frases)}.')
    if any(not row.get('frase', '').strip() for row in frases):
        raise SystemExit('Hay frases vacías en el CSV.')

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    tabla = salida.with_name(salida.stem + '_tabla_resumen.csv')
    rows = []

    rclpy.init()
    node = Node('evaluador_p1_' + str(os.getpid()))
    client = node.create_client(InterpretarOrden, '/interpretar_orden')
    try:
        if not client.wait_for_service(timeout_sec=10):
            raise SystemExit('No está disponible /interpretar_orden en el ROS_DOMAIN_ID actual.')

        with open(salida, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=SALIDA)
            writer.writeheader()
            for numero, frase in enumerate(frases, start=1):
                texto = frase['frase'].strip()
                respaldo = clasificar_respaldo(texto, args.objetos, args.colores)
                req = InterpretarOrden.Request()
                req.frase = texto
                start = time.perf_counter()
                future = client.call_async(req)
                rclpy.spin_until_future_complete(node, future, timeout_sec=args.timeout)
                elapsed_ms = round((time.perf_counter() - start) * 1000, 3)

                d = None
                error = ''
                if not future.done():
                    error = f'Sin respuesta ROS en {args.timeout}s'
                    # El servidor podría completar la solicitud más tarde.
                    try:
                        client.remove_pending_request(future)
                    except (AttributeError, ValueError):
                        pass
                else:
                    try:
                        d = future.result()
                    except Exception as exc:
                        error = str(exc)
                    if d is None and not error:
                        error = 'Respuesta ROS vacía'

                data = {k: frase.get(k, '') for k in ESPERADO}
                data.update({
                    'modo': args.modo, 'estado_solicitud': 'ok' if d else 'error',
                    'error': error,
                    'accion_respaldo': respaldo['accion'], 'objeto_respaldo': respaldo['objeto'],
                    'color_respaldo': respaldo['color'], 'prioridad_respaldo': respaldo['prioridad'],
                    'permitido_respaldo': respaldo['permitido'],
                    'acierto_respaldo_4campos': coincidencia(respaldo, frase),
                    'latencia_servicio_cliente_ms': elapsed_ms,
                    'accion_laya': '', 'objeto_laya': '', 'color_laya': '',
                    'prioridad_laya': '', 'permitido_laya': '', 'fuente': '',
                    'degradada': '', 'latencia_http_ms': '', 'inferencia_ms': '',
                    'resto_http_ms': '', 'acierto_laya_4campos': '', 'motivo': '',
                })
                if d:
                    data.update({
                        'accion_laya': d.accion, 'objeto_laya': d.objeto,
                        'color_laya': d.color, 'prioridad_laya': d.prioridad,
                        'permitido_laya': d.permitido, 'fuente': d.fuente,
                        'degradada': d.degradada,
                        'latencia_http_ms': d.latencia_http_ms,
                        'inferencia_ms': d.inferencia_ms,
                        'resto_http_ms': d.resto_http_ms, 'motivo': d.motivo,
                    })
                    if not d.degradada and d.fuente == 'LAYA':
                        data['acierto_laya_4campos'] = coincidencia({
                            'accion': d.accion, 'objeto': d.objeto,
                            'color': d.color, 'permitido': d.permitido,
                        }, frase)
                writer.writerow(data)
                file.flush()  # Preservar resultados incluso si una evaluación es interrumpida.
                rows.append(data)
                print(f'[{numero:02d}/50] {args.modo}: {data["fuente"] or "sin respuesta"}, '
                      f'{elapsed_ms:.1f} ms', flush=True)
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

    resumen = []
    for metrica in ('latencia_servicio_cliente_ms', 'latencia_http_ms',
                    'inferencia_ms', 'resto_http_ms'):
        valores = []
        for row in rows:
            try:
                value = float(row[metrica])
            except (TypeError, ValueError):
                continue
            if value >= 0 and math.isfinite(value):
                valores.append(value)
        mediana, p95 = mediana_p95(valores)
        resumen.append({'modo': args.modo, 'metrica': metrica, 'n': len(valores),
                        'mediana_ms': mediana, 'p95_ms': p95, 'aciertos': '',
                        'exactitud_pct': ''})

    for col, etiqueta in (('acierto_laya_4campos', 'exactitud_laya_real_4campos'),
                         ('acierto_respaldo_4campos', 'exactitud_respaldo_4campos')):
        evaluables = [r[col] for r in rows if isinstance(r[col], bool)]
        correctas = sum(evaluables)
        resumen.append({'modo': args.modo, 'metrica': etiqueta,
                        'n': len(evaluables), 'mediana_ms': '', 'p95_ms': '',
                        'aciertos': correctas, 'exactitud_pct':
                        round(correctas * 100. / len(evaluables), 2) if evaluables else ''})

    with open(tabla, 'w', newline='', encoding='utf-8') as file:
        campos = ['modo', 'metrica', 'n', 'mediana_ms', 'p95_ms', 'aciertos', 'exactitud_pct']
        writer = csv.DictWriter(file, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resumen)

    n_reales = sum(r['fuente'] == 'LAYA' and r['degradada'] is False for r in rows)
    n_respaldo = sum(r['fuente'] == 'respaldo' for r in rows)
    print('\nResultados de 50 frases:', salida)
    print('Tabla de latencia y exactitud:', tabla)
    print(f'LAYA real: {n_reales}/50; respaldo: {n_respaldo}/50; sin respuesta: {50-n_reales-n_respaldo}/50')
    for r in resumen:
        print(r)
    print('NOTA: resto_http_ms = HTTP - inferencia; incluye cola y procesamiento, NO solo red.')
    print('NOTA: exactitud de 4 campos excluye prioridad. No reportar exactitud sin etiquetas.')
    if n_reales != 50:
        print('ATENCIÓN: no hay 50 inferencias LAYA reales; reportar cobertura y degradaciones.')


if __name__ == '__main__':
    main()
