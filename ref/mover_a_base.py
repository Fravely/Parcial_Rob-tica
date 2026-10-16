#!/usr/bin/env python3
"""Lleva el JetCobot a la posición base (todos los ángulos en 0) y comprueba que llegó.

Se corre EN EL JETSON, con el puerto serie libre (sin sync_plan_nx corriendo).

    python3 mover_a_base.py
    python3 mover_a_base.py --velocidad 20 --si
"""
import argparse
import math
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
for _ruta in (os.path.join(AQUI, '..', 'src', 'arm_broker'), AQUI):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)
try:
    from arm_broker import fk
except ImportError:
    import fk
from brazo_util import conectar, dist, esperar_reposo, leer

BASE_DEG = [0.0] * 6


def ir_a_base(brazo, velocidad=30):
    """Devuelve (q_leido_deg, ok). ok = todos los ángulos a menos de 1 grado de cero."""
    brazo.send_angles(BASE_DEG, velocidad)
    q = esperar_reposo(brazo)
    ok = q is not None and max(abs(v) for v in q) < 1.0
    return q, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--puerto', default='', help='vacío = buscar /dev/ttyUSB0, ttyACM0, ttyTHS1...')
    ap.add_argument('--baud', type=int, default=0, help='0 = probar 1000000 y 115200')
    ap.add_argument('--velocidad', type=int, default=30)
    ap.add_argument('--si', action='store_true', help='no pedir confirmación')
    ap.add_argument('--simular', action='store_true')
    args = ap.parse_args()

    print('AVISO: el brazo va a moverse a la base. Despeja el área y avisa en voz alta.')
    print('       sync_plan_nx NO debe estar corriendo (el puerto serie es exclusivo).')
    if not args.si:
        input('ENTER para continuar, Ctrl+C para cancelar... ')

    brazo = conectar(args.puerto, args.baud, args.simular)
    antes = leer(brazo.get_angles, 6)
    print(f'Ángulos antes (grados): {antes}')

    print('Yendo a la base (todos los ángulos en 0)...')
    q, ok = ir_a_base(brazo, args.velocidad)
    if q is None:
        sys.exit('No pude leer los ángulos después de mover.')
    print(f'Ángulos ahora (grados): {q}')
    print('BASE ALCANZADA' if ok else
          'OJO: algún ángulo quedó a más de 1° de cero. Repite o revisa que nada bloquee el brazo.')

    coords = leer(brazo.get_coords, 6)
    fx, fy, fz = fk.fk([math.radians(v) for v in q])
    print(f'Tu FK en la base       : ({fx:.1f}, {fy:.1f}, {fz:.1f}) mm')
    if coords:
        e = dist((fx, fy, fz), coords[:3])
        print(f'get_coords() del brazo : ({coords[0]:.1f}, {coords[1]:.1f}, {coords[2]:.1f}) mm')
        print(f'Error FK en la base    : {e:.2f} mm   (criterio ≤ 10 mm)')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
