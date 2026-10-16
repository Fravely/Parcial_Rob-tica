#!/usr/bin/env python3
"""Monitor visual de la Pregunta 3: confirma recepción de texto desde Gemini.

Uso en el JetCobot (ROS 2 Humble):
  source /opt/ros/humble/setup.bash
  export ROS_DOMAIN_ID=72
  export ROS_LOCALHOST_ONLY=0
  cd ~/logistica && source install/setup.bash
  python3 ~/monitor_voz_api.py

Escucha /voz/transcripcion y /voz/estado; NO acciona el robot ni necesita broker.
"""

import datetime
import json
import os

VERDE = '\033[1;32m'
AMARILLO = '\033[1;33m'
ROJO = '\033[1;31m'
AZUL = '\033[1;36m'
NEGRITA = '\033[1m'
RESET = '\033[0m'


def _pintar(mensaje, color):
    if 'NO_COLOR' in os.environ:
        return mensaje
    return f'{color}{mensaje}{RESET}'


def formatear_transcripcion(cadena):
    """Devuelve el texto que aparece en terminal a partir del JSON de /voz/transcripcion."""
    hora = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        datos = json.loads(cadena)
    except (ValueError, TypeError):
        return _pintar(f'[{hora}] Mensaje no válido: {cadena}', ROJO)

    modo = str(datos.get('modo', '')).lower()
    texto = str(datos.get('texto') or '').strip()
    modelo = str(datos.get('modelo') or 'sin modelo')
    numero = datos.get('n', '?')
    ms = datos.get('transcripcion_ms', '')

    if modo == 'voz' and texto:
        color, titulo = VERDE, '✓ GEMINI RESPONDIÓ: VOZ → TEXTO'
    elif modo == 'texto':
        color, titulo = AMARILLO, '⚠ MODO TECLADO: NO CONFIRMA ACCESO A GEMINI'
    else:
        color, titulo = ROJO, '✗ SIN TRANSCRIPCIÓN VÁLIDA DE VOZ'

    linea1 = _pintar('━' * 65, color)
    linea2 = _pintar(f'[{hora}] {titulo}   | Orden {numero}', color)
    linea3 = _pintar(f'  «{texto if texto else "(vacío)"}»', color)
    linea4 = f'  Modo: {modo or "desconocido"} · Modelo: {modelo}'
    if ms != '':
        linea4 += f' · Tiempo: {ms} ms'
    return '\n'.join([linea1, linea2, linea3, linea4, linea1])


def main():
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String

    class MonitorVoz(Node):
        def __init__(self):
            super().__init__('monitor_voz_api')
            self.create_subscription(String, '/voz/transcripcion', self.al_texto, 10)
            self.create_subscription(String, '/voz/estado', self.al_estado, 10)
            print(_pintar('MONITOR VOZ/API | Esperando órdenes dictadas...', AZUL), flush=True)
            print('ROS_DOMAIN_ID=' + os.environ.get('ROS_DOMAIN_ID', '(sin configurar)'), flush=True)
            print('Verde = Google devolvió texto. Amarillo = teclado. Ctrl+C = salir.\n', flush=True)

        def al_texto(self, msg):
            print('\n' + formatear_transcripcion(msg.data) + '\n', flush=True)

        def al_estado(self, msg):
            if msg.data.startswith('MODO_TEXTO:'):
                print(_pintar('⚠ ' + msg.data, AMARILLO), flush=True)
            else:
                print(_pintar('ESTADO: ' + msg.data, NEGRITA), flush=True)

    rclpy.init()
    nodo = MonitorVoz()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
