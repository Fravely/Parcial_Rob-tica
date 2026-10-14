#!/usr/bin/env python3
"""Funciones comunes de los scripts del brazo: conectar, leer con reintentos, esperar reposo."""
import importlib
import math
import os
import sys
import time

PUERTOS_CANDIDATOS = ['/dev/ttyUSB0', '/dev/ttyACM0', '/dev/ttyTHS1', '/dev/ttyAMA0']


def _clase_mycobot():
    for modulo, nombre in (('pymycobot.mycobot', 'MyCobot'), ('pymycobot', 'MyCobot'),
                           ('pymycobot', 'MyCobot280')):
        try:
            return getattr(importlib.import_module(modulo), nombre)
        except Exception:
            continue
    sys.exit('No pude importar pymycobot.  pip3 install pymycobot --user')


def dist(a, b):
    """Distancia euclidiana (math.dist solo existe desde Python 3.8)."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _valida(v, n):
    return (isinstance(v, (list, tuple)) and len(v) >= n
            and all(isinstance(x, (int, float)) for x in v[:n]))


def leer(fn, n, intentos=10, pausa=0.3):
    """Llama fn() (get_angles / get_coords) hasta obtener n numeros validos."""
    for _ in range(intentos):
        v = fn()
        if _valida(v, n) and not all(x == -1 for x in v[:n]):
            return [float(x) for x in v[:n]]
        time.sleep(pausa)
    return None


def conectar(puerto, baud=0, simular=False):
    """Abre el puerto. Con baud=0 prueba 1000000 y luego 115200 y se queda con el que responde."""
    if simular:
        from brazo_simulado import BrazoSimulado
        print('*** MODO SIMULACION: no hay brazo real, los numeros son de ensayo ***')
        return BrazoSimulado()
    MyCobot = _clase_mycobot()
    puertos = [puerto] if puerto else [p for p in PUERTOS_CANDIDATOS if os.path.exists(p)]
    if not puertos:
        sys.exit('No hay ningún puerto serie del brazo (ls /dev/ttyUSB* /dev/ttyACM* /dev/ttyTHS1).')
    for pto in puertos:
        for b in ([baud] if baud else [1000000, 115200]):
            try:
                brazo = MyCobot(pto, b)
            except Exception as e:
                print(f'  no pude abrir {pto} a {b}: {e}')
                continue
            time.sleep(1.0)
            try:
                brazo.power_on()
            except Exception:
                pass
            time.sleep(0.5)
            if leer(brazo.get_angles, 6, intentos=4) is not None:
                print(f'Conectado a {pto} a {b} baudios.')
                return brazo
            try:
                brazo._serial_port.close()
            except Exception:
                pass
    sys.exit(f'El brazo no responde en {", ".join(puertos)}.\n'
             '  - ¿sync_plan_nx sigue corriendo? Detenlo (Ctrl+C en su terminal).\n'
             '  - ¿Puerto correcto? ls /dev/ttyUSB* /dev/ttyACM* /dev/ttyTHS1\n'
             '  - ¿Otro integrante tiene el puerto abierto?\n'
             '  - Si ves "Permission denied": NO cambies permisos; consulta al profesor.')


def esperar_reposo(brazo, timeout=25.0, tol=0.2, estables=3):
    """Espera a que los angulos dejen de cambiar. Mas fiable que un sleep fijo."""
    rapido = getattr(brazo, 'simulado', False)
    time.sleep(0.1 if rapido else 1.0)
    previo, cuenta, t0 = None, 0, time.time()
    while time.time() - t0 < timeout:
        q = leer(brazo.get_angles, 6, intentos=3)
        if q is not None and previo is not None:
            cuenta = cuenta + 1 if max(abs(a - b) for a, b in zip(q, previo)) < tol else 0
            if cuenta >= estables:
                return q
        previo = q if q is not None else previo
        time.sleep(0.02 if rapido else 0.4)
    return leer(brazo.get_angles, 6)
