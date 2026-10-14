#!/usr/bin/env python3
"""Calcula los planes de un color SIN mover el brazo, SIN abrir el puerto y SIN camara.

El inicio es la pose de escaneo HIPOTETICA (no una lectura del robot). Sirve para
revisar las trayectorias con el modelo del laboratorio antes de autorizar movimiento,
y para contar cuantos puntos trae cada plan (de ahi sale el tiempo real del pedido).

    python3 herramientas/previsualizar_item2.py --config plantillas/item2_calibrado.json \
        --color rojo --salida evidencias/plan_rojo.json
"""
import argparse
import json
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/arm_broker'))


def main():
    import rclpy
    from rclpy.node import Node
    from rclpy.executors import MultiThreadedExecutor
    from arm_broker.broker import (cargar_montaje, radianes, Planificador,
                                   ordenar_articulaciones)

    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', default='plantillas/item2_montaje.json')
    p.add_argument('--color', choices=['amarillo', 'azul', 'verde', 'rojo'], required=True)
    p.add_argument('--grupo', default='arm_group')
    p.add_argument('--enlace', default='6_Link')
    p.add_argument('--marco', default='base_link')
    p.add_argument('--salida', required=True)
    a = p.parse_args()

    c = cargar_montaje(a.config, avisar=lambda m: print('AVISO: ' + m))
    rclpy.init()
    nodo = Node('previsualizar_item2_sin_movimiento')
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(nodo)
    hilo = threading.Thread(target=executor.spin, daemon=True)
    hilo.start()
    planes = []
    try:
        plan = Planificador(nodo, a.grupo, a.enlace, a.marco,
                            tolerancia_modelo_mm=c['tolerancia_modelo_mm'])
        escaneo = radianes(c['escaneo_grados'])
        agarre = radianes(c['recogida_grados'][a.color])
        deposito = radianes(c['_deposito'][a.color])
        plan.validar_modelo_rb2([escaneo, agarre, deposito], lambda: False)
        print('FK del RB-2 y FK del URDF coinciden dentro de '
              f'{c["tolerancia_modelo_mm"]:.0f} mm')
        actual = escaneo[:]
        altura = c['altura_aproximacion_mm']
        etapas = [('preagarre', agarre, altura), ('agarre', agarre, 0),
                  ('levantar', agarre, altura), ('predeposito', deposito, altura),
                  ('deposito', deposito, 0), ('retirar', deposito, altura),
                  ('escaneo', escaneo, 0)]
        total = 0
        for etapa, q, h in etapas:
            trayectoria, _, _ = plan.planificar_referencia(q, actual, lambda: False, print, h)
            puntos = [dict(q_rad=ordenar_articulaciones(trayectoria.joint_names, t.positions),
                           tiempo_moveit_s=t.time_from_start.sec
                           + t.time_from_start.nanosec / 1e9)
                      for t in trayectoria.points]
            planes.append(dict(etapa=etapa, puntos=puntos))
            total += len(puntos)
            print(f'{etapa}: {len(puntos)} puntos, '
                  f'{puntos[-1]["tiempo_moveit_s"]:.2f} s segun MoveIt2')
            actual = puntos[-1]['q_rad']
        salida = Path(a.salida)
        salida.parent.mkdir(parents=True, exist_ok=True)
        salida.write_text(json.dumps(dict(
            solo_planificacion=True, inicio_hipotetico_grados=c['escaneo_grados'],
            color=a.color, puntos_totales=total, planes=planes), indent=2), encoding='utf-8')
        print(f'\n{total} puntos en total para un pedido completo.')
        print('El broker reproduce TODOS con lectura real en cada uno: el pedido tarda mas')
        print('que el tiempo de MoveIt2. Si sale muy lento, sube tolerancia_intermedia_grados.')
        print('Planes guardados SIN EJECUTAR: ' + str(salida))
    finally:
        executor.shutdown()
        hilo.join(3)
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
