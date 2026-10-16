#!/usr/bin/env python3
"""Solo lectura. No abre el puerto serie, no lanza controladores ni mueve el robot."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess

def consultar(titulo, argumentos):
    print('\n' + titulo, flush=True)
    if shutil.which(argumentos[0]) is None:
        print('NO DISPONIBLE: ' + argumentos[0]); return
    try:
        r = subprocess.run(argumentos, capture_output=True, text=True, timeout=12)
        print((r.stdout + r.stderr).strip() or '(sin salida)')
        print('codigo_salida=' + str(r.returncode))
    except subprocess.TimeoutExpired:
        print('TIEMPO LIMITE; no implica que el servicio no exista')

print('DIAGNOSTICO ITEM 2 - SIN MOVIMIENTO')
print('ROS_DISTRO=' + os.environ.get('ROS_DISTRO','NO CARGADO'))
print('ROS_DOMAIN_ID=' + os.environ.get('ROS_DOMAIN_ID','NO DEFINIDO') + ' (equipo: 52)')
for nombre in ('pymycobot', 'cv2', 'rclpy'):
    try:
        encontrado = importlib.util.find_spec(nombre) is not None
    except (ImportError, ValueError):
        encontrado = False
    print(nombre + ': ' + ('disponible' if encontrado else 'no disponible'))
consultar('Procesos que usan el puerto', ['fuser','-v','/dev/ttyUSB0'])
consultar('Nodos ROS', ['ros2','node','list'])
consultar('Servicios y tipos (buscar compute_fk, compute_ik, plan_kinematic_path)',
          ['ros2','service','list','-t'])
consultar('Acciones y tipos', ['ros2','action','list','-t'])
consultar('Publicadores y suscriptores del topic usado por el broker RB2',
          ['ros2','topic','info','/joint_states','-v'])
consultar('Paquetes MoveIt y JetCobot instalados', ['ros2','pkg','list'])
print('\nArchivos de lanzamiento candidatos (solo listar, NO ejecutar)')
for base in (Path('/opt/ros/humble/share'), Path.home()/'jetcobot_ws/install'):
    if base.is_dir():
        for d in sorted(base.glob('*')):
            if 'moveit' in d.name.lower() or 'jetcobot' in d.name.lower():
                for p in d.glob('**/launch/*.launch.py'):
                    print(p)
print('\nNo se ejecuto ningun movimiento. Compartir esta salida antes de elegir el launch.')
