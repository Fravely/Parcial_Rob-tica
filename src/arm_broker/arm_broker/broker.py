"""arm_broker — EL MISMO broker del RB-2, ampliado para el examen parcial, en UN archivo.

No es una implementación nueva: conserva el andamiaje del curso y los bloques que se
calificaron en el RB-2 (goal_callback, handle_accepted_callback, _worker,
execute_callback, las políticas de cola y la FK del RB-2), con los mismos nombres y la
misma lógica. Lo añadido para la Pregunta 2 es la acción PickPlace y lo que cuelga de
ella: reconocimiento de color en imagen completa, IK y planificación con MoveIt2, ejecución física
por pymycobot y la evidencia de los diez intentos.

Sigue valiendo la regla del RB-2: UN portero (goal_callback) decide quién entra, UNA sala
de espera (self.pendientes) guarda a los aceptados, y UN trabajador (_worker) atiende de a
uno. Ningún otro nodo ni hilo toca el brazo.

Secciones de este archivo
  1. Cinemática directa del RB-2            6. Planificación con MoveIt2 (IK + trayectoria)
  2. Políticas de cola (RB-2)               7. Secuencia física de pick & place
  3. Errores y utilidades                   8. Secuencia simulada
  4. Montaje: poses enseñadas               9. Evidencia de los diez intentos
  5. Visión como el notebook 5             10. Nodo ROS 2 ArmBroker

Modos (excluyentes; por defecto NO se mueve nada):
  simulado   habilitar_pick_place_simulado:=true   etapas falsas, sin cámara ni brazo
  plan       habilitar_planificacion_pick_place:=true   IK y trayectoria, nunca ejecuta
  físico     habilitar_pick_place_fisico:=true     cámara + MoveIt2 + brazo real

Las dependencias pesadas (moveit_msgs, cv2, pymycobot) se importan solo dentro del modo
que las necesita: en simulación este archivo corre en cualquier equipo.
"""

import csv
import json
import math
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from sensor_msgs.msg import JointState

from arm_broker_interfaces.action import MoveArm, PickPlace
from arm_broker_interfaces.msg import QueueState


# ==========================================================================
# 1. Cinemática directa del RB-2
# --------------------------------------------------------------------------
# Convención: DH ESTÁNDAR. Cada fila es (alpha_rad, a_mm, d_mm, theta_offset_rad) y la
# matriz de cada eslabón es la de _t(). Tabla y matriz van de la mano: no mezclar esta
# tabla con una matriz de DH modificada (la de Craig) ni al revés.
# Es la misma tabla de fk.py; _verificar_fk_externa() avisa si alguien cambia una sola.
# ==========================================================================

JOINT_NAMES = ['1_Joint', '2_Joint', '3_Joint', '4_Joint', '5_Joint', '6_Joint']

DH = [
    (math.pi / 2.0,   0.0,    132.5,    0.0),
    (0.0,            -111.5,  0.0,     -math.pi / 2.0),
    (0.0,            -95.0,   0.0,      0.0),
    (math.pi / 2.0,   0.0,    65.5,    -math.pi / 2.0),
    (-math.pi / 2.0,  0.0,    74.0,     math.pi / 2.0),
    (0.0,             0.0,    49.5,     0.0),
]

JOINT_LIMITS = [
    (-2.93, 2.93),
    (-2.36, 2.36),
    (-2.53, 2.53),
    (-2.58, 2.58),
    (-2.93, 2.93),
    (-3.14, 3.14),
]

ALCANCE_MIN_MM = 80.0
ALCANCE_MAX_MM = 480.0


def _t(alpha, a, d, theta):
    """Transformación homogénea 4x4 de un eslabón (DH estándar)."""
    ca, sa = math.cos(alpha), math.sin(alpha)
    ct, st = math.cos(theta), math.sin(theta)
    return [
        [ct,  -st * ca,   st * sa,  a * ct],
        [st,   ct * ca,  -ct * sa,  a * st],
        [0.0,  sa,        ca,       d],
        [0.0,  0.0,       0.0,      1.0],
    ]


def _mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def fk_matriz(q):
    """Matriz homogénea 4x4 de la base al efector final. q en radianes (6 valores)."""
    if len(q) != 6:
        raise ValueError(f'se esperaban 6 ángulos, llegaron {len(q)}')
    T = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for (alpha, a, d, off), theta in zip(DH, q):
        T = _mul(T, _t(alpha, a, d, theta + off))
    return T


def fk(q):
    """Posición (x, y, z) del efector final en mm, respecto a la base."""
    T = fk_matriz(q)
    return T[0][3], T[1][3], T[2][3]


def dentro_de_limites(q):
    if len(q) != 6:
        return False, f'se esperaban 6 ángulos, llegaron {len(q)}'
    for i, (valor, (lo, hi)) in enumerate(zip(q, JOINT_LIMITS)):
        if not lo <= valor <= hi:
            return False, f'{JOINT_NAMES[i]} fuera de rango: {valor:.3f} rad, límite [{lo}, {hi}]'
    return True, ''


def margen_a_limites(q):
    """Grados que sobran hasta el límite más cercano. Avisa de poses al borde."""
    peor, articulacion = 1e9, ''
    for i, (valor, (lo, hi)) in enumerate(zip(q, JOINT_LIMITS)):
        margen = min(valor - lo, hi - valor)
        if margen < peor:
            peor, articulacion = margen, JOINT_NAMES[i]
    return math.degrees(peor), articulacion


def dentro_del_workspace(q):
    x, y, z = fk(q)
    r = math.sqrt(x * x + y * y + z * z)
    if r > ALCANCE_MAX_MM:
        return False, f'efector a {r:.0f} mm de la base, máximo {ALCANCE_MAX_MM:.0f}'
    if r < ALCANCE_MIN_MM:
        return False, f'efector a {r:.0f} mm de la base, demasiado cerca'
    if z < 0.0:
        return False, f'z = {z:.0f} mm: el efector quedaría bajo la base'
    return True, ''


def paso_articular(q_desde, q_hasta):
    return max(abs(b - a) for a, b in zip(q_desde, q_hasta))


def _verificar_fk_externa():
    """fk.py sigue existiendo para orden_a_broker, generar_carga y las pruebas.

    Si alguien edita una tabla y no la otra, los números del informe dejarían de
    corresponder. Devuelve el aviso, o '' si coinciden o si fk.py ya no está.
    """
    try:
        from arm_broker import fk as externo
    except Exception:
        return ''
    if list(externo.JOINT_NAMES) != JOINT_NAMES:
        return 'arm_broker/fk.py usa otros nombres de articulación'
    if [tuple(f) for f in externo.DH] != [tuple(f) for f in DH]:
        return 'arm_broker/fk.py tiene OTRA tabla DH: las FK no coincidirán'
    if [tuple(l) for l in externo.JOINT_LIMITS] != [tuple(l) for l in JOINT_LIMITS]:
        return 'arm_broker/fk.py tiene OTROS límites articulares'
    return ''


# ==========================================================================
# 2. Políticas de cola — RB-2 ítems 2 y 3 (sin cambios respecto al RB-2)
# ==========================================================================

class Pedido:
    def __init__(self, goal_handle, client_id, priority, joint_positions):
        self.goal_handle = goal_handle
        self.goal_id = bytes(goal_handle.goal_id.uuid).hex()[:12]
        self.client_id = client_id
        self.priority = int(priority)
        self.joint_positions = list(joint_positions)
        self.t_llegada = time.time()
        self.t_inicio_ejec = None
        self.fin = threading.Event()
        self.resultado = None
        self.tipo_pick = False
        self.trabajo_fisico = None
        self.esperando_fisico = False

    @property
    def espera_s(self):
        fin = self.t_inicio_ejec if self.t_inicio_ejec else time.time()
        return fin - self.t_llegada

    def __repr__(self):
        return f'<{self.client_id} p{self.priority} {self.goal_id}>'


class Politica:
    nombre = 'base'

    def siguiente(self, pendientes):
        raise NotImplementedError

    def atendido(self, pedido):
        pass


class FIFO(Politica):
    """Atiende en orden de llegada."""
    nombre = 'fifo'

    def siguiente(self, pendientes):
        if not pendientes:
            return None
        return min(range(len(pendientes)), key=lambda i: pendientes[i].t_llegada)


class SegundaPolitica(Politica):
    """Prioridad con envejecimiento.

    puntaje = prioridad + espera_s / tau   (mayor puntaje = se atiende antes)
    Cada tau segundos de espera equivalen a subir un nivel de prioridad, así que la
    espera de un pedido de prioridad p queda acotada a ~ (p_max - p) * tau más lo que
    dure el movimiento en curso. Empate: gana el que llegó antes.
    """
    nombre = 'prioridad'

    def __init__(self, tau_envejecimiento_s=8.0):
        self.tau = max(1e-3, float(tau_envejecimiento_s))

    def puntaje(self, pedido):
        return pedido.priority + pedido.espera_s / self.tau

    def siguiente(self, pendientes):
        if not pendientes:
            return None
        return max(range(len(pendientes)),
                   key=lambda i: (self.puntaje(pendientes[i]), -pendientes[i].t_llegada))


POLITICAS = {'fifo': FIFO, 'prioridad': SegundaPolitica}


# ==========================================================================
# 3. Errores y utilidades
# --------------------------------------------------------------------------
# La diferencia IMPORTA: un ErrorDePedido (no hay cubo de ese color, el depósito está
# ocupado, la entrega no se confirmó) termina ESE intento con success=False y el broker
# sigue atendiendo. Un ErrorDeHardware (serial, el brazo no llega, la parada no se
# confirma) deja el brazo en estado desconocido: se enclava y se exige revisar y
# reiniciar. Antes cualquier fallo enclavaba, y un cubo retirado dejaba la demostración
# muerta para el resto de la evaluación.
# ==========================================================================

class Cancelado(Exception):
    pass


class ErrorDePedido(Exception):
    """El intento falla, el brazo queda en una pose conocida y se puede seguir."""


class ErrorDeHardware(Exception):
    """El brazo puede haber quedado a medias: no se admiten más pedidos físicos."""


def seis_finitos(valores, nombre):
    if not isinstance(valores, (list, tuple)) or len(valores) != 6:
        raise ValueError(nombre + ': se requieren seis valores')
    if not all(type(v) in (int, float) and math.isfinite(v) for v in valores):
        raise ValueError(nombre + ': todos los valores deben ser numeros finitos')
    return list(map(float, valores))


def cargar_objetivos(texto):
    datos = json.loads(texto)
    if not isinstance(datos, dict):
        raise ValueError('objetivos_planificacion_json debe ser un objeto JSON')
    return {k: seis_finitos(v, k) for k, v in datos.items()}


def quaternion_rpy_grados(rpy):
    r, p, y = [math.radians(v) / 2 for v in rpy]
    cr, sr = math.cos(r), math.sin(r)
    cp, sp = math.cos(p), math.sin(p)
    cy, sy = math.cos(y), math.sin(y)
    return (sr * cp * cy - cr * sp * sy, cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy, cr * cp * cy + sr * sp * sy)


def ordenar_articulaciones(nombres, posiciones):
    if len(nombres) != len(posiciones) or len(set(nombres)) != len(nombres):
        raise ValueError('estado articular incompleto o duplicado')
    tabla = dict(zip(nombres, posiciones))
    try:
        q = seis_finitos([tabla[n] for n in JOINT_NAMES], 'estado articular')
    except KeyError as exc:
        raise ValueError('falta articulacion ' + str(exc)) from exc
    ok, motivo = dentro_de_limites(q)
    if not ok:
        raise ValueError(motivo)
    return q


def validar_trayectoria(trayectoria, inicio, destino):
    if not trayectoria.points:
        raise ValueError('MoveIt2 devolvio una trayectoria vacia')
    if set(trayectoria.joint_names) != set(JOINT_NAMES):
        raise ValueError('trayectoria no corresponde a las seis articulaciones del brazo')
    puntos, anterior = [], -1.0
    for punto in trayectoria.points:
        q = ordenar_articulaciones(trayectoria.joint_names, punto.positions)
        t = punto.time_from_start.sec + punto.time_from_start.nanosec / 1e9
        if not math.isfinite(t) or t < 0 or t <= anterior:
            raise ValueError('tiempos de trayectoria no crecientes')
        anterior = t
        puntos.append(q)
    if paso_articular(puntos[0], inicio) > 0.02:
        raise ValueError('trayectoria no comienza en el estado solicitado')
    if paso_articular(puntos[-1], destino) > 0.02:
        raise ValueError('trayectoria no termina en la solucion IK')
    return puntos


# ==========================================================================
# 4. Montaje: poses enseñadas en grados. No importa ROS ni abre hardware.
# ==========================================================================

COLORES = ('amarillo', 'azul', 'verde', 'rojo')
MARGEN_LIMITE_AVISO_GRADOS = 2.0


def radianes(grados):
    q = [math.radians(v) for v in seis_finitos(grados, 'pose en grados')]
    ok, motivo = dentro_de_limites(q)
    if not ok:
        raise ValueError(motivo)
    return q


def cargar_montaje(archivo, fisico=False, avisar=None):
    """Cuatro lugares fisicos; el color se determina al ejecutar cada pedido."""
    with open(archivo, encoding='utf-8') as f:
        c = json.load(f)
    c['_deposito'] = {color: list(c['deposito_grados']) for color in COLORES}
    posiciones = c.get('posiciones_recogida')
    if not isinstance(posiciones, dict) or len(posiciones) != 4:
        raise ValueError('configura las cuatro posiciones_recogida en poses_sin_laya.json')
    for nombre, lugar in posiciones.items():
        radianes(lugar['grados'])
        roi = lugar['roi_normalizada']
        if (len(roi) != 4 or not all(math.isfinite(v) for v in roi)
                or not (0 <= roi[0] < roi[2] <= 1 and 0 <= roi[1] < roi[3] <= 1)):
            raise ValueError('region de imagen invalida: ' + nombre)
    for pose in [c['deposito_grados'], c['escaneo_grados'], c['home_grados']]:
        radianes(pose)
    c.setdefault('tolerancia_intermedia_grados', 3.0)
    return c


# ==========================================================================
# 5. Visión: reconoce el color pedido en la imagen completa, desde escaneo.
# --------------------------------------------------------------------------
# Cada color se asocia a su pose fija enseñada. No estima coordenadas desde píxeles.
# ==========================================================================

RANGOS = {
    'amarillo': ([(20, 35)], 80, 80),
    'rojo': ([(0, 10), (170, 179)], 80, 50),
    'verde': ([(40, 80)], 110, 60),
    'azul': ([(105, 135)], 110, 60),
}


def area_color(frame, color):
    """Mismos umbrales HSV y contorno mayor que el notebook 5; imagen completa."""
    import cv2 as cv
    import numpy as np
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    bandas, s, v = RANGOS[color]
    mascara = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for inferior, superior in bandas:
        mascara |= cv.inRange(hsv, (inferior, s, v), (superior, 255, 255))
    contornos, _ = cv.findContours(mascara, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return max((cv.contourArea(c) for c in contornos), default=0.0)


def localizar_color(frame, color, c):
    """Clasifica cada lugar de la imagen actual, sin asociar colores a poses."""
    alto, ancho = frame.shape[:2]
    posiciones = {}
    candidatos = []
    for nombre, lugar in c['posiciones_recogida'].items():
        x0, y0, x1, y1 = lugar['roi_normalizada']
        ix0, iy0 = int(x0 * ancho), int(y0 * alto)
        ix1, iy1 = int(x1 * ancho), int(y1 * alto)
        region = frame[iy0:iy1, ix0:ix1]
        areas = {tono: float(area_color(region, tono)) for tono in COLORES}
        orden = sorted(areas, key=areas.get, reverse=True)
        primero, segundo = orden[:2]
        # Umbral escalado respecto de la foto de referencia (752 x 562).
        minimo = max(float(c['area_minima_px']) * ancho * alto / (752 * 562),
                     0.04 * (ix1 - ix0) * (iy1 - iy0))
        valido = areas[primero] > minimo and areas[primero] > 1.5 * areas[segundo]
        detectado = primero if valido else None
        posiciones[nombre] = dict(color=detectado, areas_px=areas,
                                 roi_px=[ix0, iy0, ix1, iy1])
        if detectado == color:
            candidatos.append(nombre)
    elegido = candidatos[0] if len(candidatos) == 1 else None
    motivo = ('color encontrado en mas de una posicion' if len(candidatos) > 1
              else 'color no localizado con claridad en las cuatro posiciones')
    return dict(color=color, detectado=elegido is not None, posicion=elegido,
                posiciones=posiciones, motivo='' if elegido else motivo,
                area_px=posiciones[elegido]['areas_px'][color] if elegido else 0.0)


def capturar_sin_mover(solicitud):
    """Una captura al atender el pedido; sin calibración ni vista del depósito."""
    import cv2 as cv
    c = solicitud['config']
    cap = cv.VideoCapture(c['camara'])
    try:
        if not cap.isOpened():
            raise RuntimeError('no se puede abrir la camara')
        for _ in range(5):
            cap.read()
        ok, frame = cap.read()
        if not ok or frame is None:
            raise RuntimeError('no se recibio imagen de la camara')
        observacion = localizar_color(frame, solicitud['color'], c)
        archivo = Path(solicitud['carpeta']) / (solicitud['etiqueta'] + '.png')
        if not cv.imwrite(str(archivo), frame):
            raise OSError('no se pudo guardar la captura')
        return observacion
    finally:
        cap.release()


class VisionFija:
    def __init__(self, configuracion):
        self.c = configuracion

    def observar(self, color, cancelado, carpeta, etiqueta):
        carpeta = Path(carpeta)
        carpeta.mkdir(parents=True, exist_ok=True)
        entrada = carpeta / (etiqueta + '_solicitud.json')
        salida = carpeta / (etiqueta + '_vision.json')
        entrada.write_text(json.dumps({
            'config': self.c, 'color': color,
            'carpeta': str(carpeta), 'etiqueta': etiqueta}), encoding='utf-8')
        proceso = subprocess.Popen(
            [sys.executable, '-m', 'arm_broker.broker', '--captura', str(entrada), str(salida)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        limite = time.monotonic() + 15
        try:
            while proceso.poll() is None:
                if cancelado():
                    raise Cancelado('cancelado durante captura')
                if time.monotonic() > limite:
                    raise ErrorDePedido('la camara no respondio en 15 segundos')
                time.sleep(0.05)
            _, error = proceso.communicate()
            if proceso.returncode:
                raise ErrorDePedido('captura fallo: ' + error.decode(errors='replace')[-500:])
            return json.loads(salida.read_text(encoding='utf-8'))
        finally:
            if proceso.poll() is None:
                proceso.kill()
                proceso.communicate()




# ==========================================================================
# 6. Planificación: FK del URDF -> objetivo cartesiano -> IK -> plan MoveIt2.
#    NUNCA ejecuta: devuelve la trayectoria para que la reproduzca el worker.
# ==========================================================================

def pose_mm_grados(pose):
    p, q = pose.position, pose.orientation
    r = math.atan2(2 * (q.w * q.x + q.y * q.z), 1 - 2 * (q.x * q.x + q.y * q.y))
    pitch = math.asin(max(-1., min(1., 2 * (q.w * q.y - q.z * q.x))))
    y = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
    return [p.x * 1000, p.y * 1000, p.z * 1000, *map(math.degrees, (r, pitch, y))]


class Planificador:
    """Cliente de /compute_fk, /compute_ik y /plan_kinematic_path. Solo planifica.

    La pose corresponde al enlace configurado, no al centro de la pinza.
    """

    def __init__(self, nodo, grupo='arm_group', enlace='6_Link', marco='base_link',
                 timeout=8.0, tolerancia_modelo_mm=10.0):
        from moveit_msgs.srv import GetPositionFK, GetPositionIK, GetMotionPlan
        self.nodo = nodo
        self.grupo = grupo
        self.enlace = enlace
        self.marco = marco
        self.timeout = timeout
        self.tolerancia_modelo_mm = tolerancia_modelo_mm
        cg = ReentrantCallbackGroup()
        self.cli_fk = nodo.create_client(GetPositionFK, '/compute_fk', callback_group=cg)
        self.cli_ik = nodo.create_client(GetPositionIK, '/compute_ik', callback_group=cg)
        self.cli_plan = nodo.create_client(GetMotionPlan, '/plan_kinematic_path',
                                           callback_group=cg)
        self.ultimo_plan = None

    def consultar(self, cli, req, cancelado):
        limite = time.monotonic() + self.timeout
        while not cli.wait_for_service(timeout_sec=0.1):
            if cancelado():
                raise Cancelado('cancelado esperando MoveIt2')
            if time.monotonic() >= limite:
                raise ErrorDePedido('servicio MoveIt2 no disponible: revisa que move_group '
                                    'este corriendo y que haya UNO solo')
        if cancelado():
            raise Cancelado('cancelado antes de consultar MoveIt2')
        futuro = cli.call_async(req)
        evento = threading.Event()
        futuro.add_done_callback(lambda _f: evento.set())
        while not evento.wait(0.02):
            if cancelado() or time.monotonic() >= limite:
                try:
                    cli.remove_pending_request(futuro)
                except Exception:
                    pass
                futuro.cancel()
                if cancelado():
                    raise Cancelado('consulta MoveIt2 cancelada localmente')
                raise ErrorDePedido('MoveIt2 supero el tiempo limite')
        if cancelado():
            raise Cancelado('cancelado al recibir respuesta MoveIt2')
        respuesta = futuro.result()
        if respuesta is None:
            raise ErrorDePedido('respuesta MoveIt2 vacia')
        return respuesta

    # --------------------------------------------------- FK del modelo de MoveIt
    def pose_ensenada(self, q, cancelado):
        from moveit_msgs.srv import GetPositionFK
        req = GetPositionFK.Request()
        req.header.frame_id = self.marco
        req.fk_link_names = [self.enlace]
        req.robot_state.is_diff = True
        req.robot_state.joint_state.name = list(JOINT_NAMES)
        req.robot_state.joint_state.position = list(q)
        r = self.consultar(self.cli_fk, req, cancelado)
        if r.error_code.val != 1 or len(r.pose_stamped) != 1 or r.fk_link_names != [self.enlace]:
            raise ErrorDePedido('FK MoveIt no devolvio el enlace esperado')
        if r.pose_stamped[0].header.frame_id != self.marco:
            raise ErrorDePedido('FK devuelta en un marco distinto')
        pose = pose_mm_grados(r.pose_stamped[0].pose)
        if not all(math.isfinite(v) for v in pose):
            raise ErrorDePedido('FK MoveIt no finita')
        return pose

    # --------------------------------------------------- IK + trayectoria
    def calcular(self, pose_objetivo, semilla, cancelado, feedback, semilla_ik=None):
        from moveit_msgs.srv import GetPositionIK, GetMotionPlan
        from moveit_msgs.msg import Constraints, JointConstraint
        self.ultimo_plan = None
        pose = seis_finitos(pose_objetivo, 'pose objetivo')
        q = ordenar_articulaciones(JOINT_NAMES, semilla)
        etapas, tiempos = [], []

        feedback('IK_MOVEIT2_SOLO_PLAN')
        inicio = time.perf_counter()
        req = GetPositionIK.Request()
        ir = req.ik_request
        ir.group_name = self.grupo
        ir.ik_link_name = self.enlace
        ir.avoid_collisions = True
        ir.robot_state.is_diff = True
        ir.robot_state.joint_state.name = list(JOINT_NAMES)
        ir.robot_state.joint_state.position = list(
            q if semilla_ik is None else ordenar_articulaciones(JOINT_NAMES, semilla_ik))
        ir.pose_stamped.header.frame_id = self.marco
        ir.pose_stamped.header.stamp = self.nodo.get_clock().now().to_msg()
        pos = ir.pose_stamped.pose.position
        pos.x, pos.y, pos.z = [v / 1000 for v in pose[:3]]
        rot = ir.pose_stamped.pose.orientation
        rot.x, rot.y, rot.z, rot.w = quaternion_rpy_grados(pose[3:])
        ir.timeout.sec = 2
        r = self.consultar(self.cli_ik, req, cancelado)
        if r.error_code.val != 1:
            raise ErrorDePedido(f'IK fallo, codigo MoveIt2={r.error_code.val}: la pose puede '
                                'estar fuera de alcance o en colision')
        destino = ordenar_articulaciones(r.solution.joint_state.name,
                                         r.solution.joint_state.position)
        etapas.append('IK_MOVEIT2_SOLO_PLAN')
        tiempos.append(time.perf_counter() - inicio)

        feedback('TRAYECTORIA_MOVEIT2_SOLO_PLAN')
        inicio = time.perf_counter()
        reqp = GetMotionPlan.Request()
        mp = reqp.motion_plan_request
        mp.group_name = self.grupo
        mp.start_state.is_diff = True
        mp.start_state.joint_state.name = list(JOINT_NAMES)
        mp.start_state.joint_state.position = list(q)
        mp.num_planning_attempts = 1
        mp.allowed_planning_time = 3.0
        mp.max_velocity_scaling_factor = 0.15
        mp.max_acceleration_scaling_factor = 0.15
        restricciones = Constraints()
        restricciones.name = 'objetivo_ik'
        for nombre, valor in zip(JOINT_NAMES, destino):
            jc = JointConstraint()
            jc.joint_name = nombre
            jc.position = valor
            jc.tolerance_above = 0.005
            jc.tolerance_below = 0.005
            jc.weight = 1.0
            restricciones.joint_constraints.append(jc)
        mp.goal_constraints = [restricciones]
        respuesta = self.consultar(self.cli_plan, reqp, cancelado).motion_plan_response
        if respuesta.error_code.val != 1:
            raise ErrorDePedido(f'planificacion fallo, codigo MoveIt2={respuesta.error_code.val}')
        if respuesta.group_name != self.grupo:
            raise ErrorDePedido('grupo devuelto por MoveIt2 no coincide')
        puntos = validar_trayectoria(respuesta.trajectory.joint_trajectory, q, destino)
        if cancelado():
            raise Cancelado('cancelado despues de planificar')
        self.ultimo_plan = respuesta.trajectory
        etapas.append('TRAYECTORIA_MOVEIT2_SOLO_PLAN')
        tiempos.append(time.perf_counter() - inicio)
        self.nodo.get_logger().info(
            f'PLAN CALCULADO: {len(puntos)} puntos; NO EJECUTADO; enlace={self.enlace}')
        return etapas, tiempos

    def planificar_referencia(self, referencia, actual, cancelado, feedback, altura=0.0):
        """Pose enseñada -> FK del URDF -> (+altura) -> IK con la pose como semilla -> plan."""
        pose = self.pose_ensenada(referencia, cancelado)
        pose[2] += altura
        etapas, tiempos = self.calcular(pose, actual, cancelado, feedback,
                                        semilla_ik=referencia)
        trayectoria = self.ultimo_plan.joint_trajectory
        ultimo = ordenar_articulaciones(trayectoria.joint_names, trayectoria.points[-1].positions)
        if altura == 0 and paso_articular(ultimo, referencia) > math.radians(5):
            raise ErrorDePedido('IK eligio otra rama distinta de la pose ensenada')
        return trayectoria, etapas, tiempos


# ==========================================================================
# 7. Hardware y secuencia física
# --------------------------------------------------------------------------
# pymycobot SOLO desde el hilo worker del broker. Los clientes nunca abren el puerto.
# ==========================================================================

class BrazoSerial:
    def __init__(self, config, telemetria):
        import fcntl
        self.c = config
        self.telemetria = telemetria
        self.mc = None
        self.cerrojo = None
        nombre = os.path.basename(config['puerto'])
        try:
            self.cerrojo = open('/tmp/logistica_' + nombre + '.lock', 'a')
            fcntl.flock(self.cerrojo, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if shutil.which('fuser') is None:
                raise ErrorDeHardware('falta el comando fuser: sudo apt install psmisc')
            r = subprocess.run(['fuser', config['puerto']], capture_output=True, timeout=5)
            if r.returncode != 1:
                raise ErrorDeHardware(
                    'el puerto ' + config['puerto'] + ' ya esta ocupado: detén el otro broker, '
                    'el driver y los notebooks (fuser -v ' + config['puerto'] + ')')
            from pymycobot.mycobot import MyCobot

            class MyCobotRecepcion(MyCobot):
                def __init__(self, *args, **kwargs):
                    self._fin_comando = None
                    self._turno_serial = threading.Lock()
                    super().__init__(*args, **kwargs)

                def _mesg(self, *args, **kwargs):
                    # Espaciar comandos y consultas, incluidos los de pinza.
                    with self._turno_serial:
                        if self._fin_comando is not None:
                            pausa = 0.05 - (time.monotonic() - self._fin_comando)
                            if pausa > 0:
                                time.sleep(pausa)
                        try:
                            return super()._mesg(*args, **kwargs)
                        finally:
                            self._fin_comando = time.monotonic()

                # pymycobot 3.4.6: el parser tiene un plazo independiente
                # del timeout de cada lectura del puerto serial.
                def _read(self, genre, method=None, command=None, _class=None, timeout=None):
                    return super()._read(
                        genre, method=method, command=command, _class=_class,
                        timeout=0.5 if timeout is None else timeout)

            self.mc = MyCobotRecepcion(config['puerto'], config['baudios'], timeout=0.1)
            # Exclusividad POSIX: no protege de un driver que ignore los bloqueos.
            self.mc._serial_port.exclusive = True
        except BlockingIOError:
            self.close()
            raise ErrorDeHardware('otro proceso de este broker ya tiene el puerto')
        except ErrorDeHardware:
            self.close()
            raise
        except Exception as exc:
            self.close()
            raise ErrorDeHardware('no se pudo abrir el brazo: ' + str(exc)) from exc

    @staticmethod
    def comprobar(cancelado):
        if cancelado():
            raise Cancelado('cancelado durante ejecucion fisica')

    def leer(self, cancelado=None, limite=None):
        """Hasta tres consultas; nunca publica ni utiliza una lectura incompleta."""
        cancelado = cancelado or (lambda: False)
        recibidos = []
        for intento in range(3):
            self.comprobar(cancelado)
            if limite is not None and time.monotonic() >= limite:
                break
            valores = self.mc.get_angles()
            self.comprobar(cancelado)
            recibidos.append(repr(valores))
            if isinstance(valores, (list, tuple)) and len(valores) == 6:
                try:
                    q = radianes(valores)
                except (ValueError, TypeError) as exc:
                    raise ErrorDeHardware('lectura articular invalida: ' + str(exc)) from exc
                if limite is not None and time.monotonic() >= limite:
                    break
                self.telemetria(q)
                return q
            print('Lectura get_angles incompleta: ' + repr(valores) +
                  '; intento ' + str(intento + 1) + '/3', flush=True)
            if intento < 2:
                time.sleep(0.15)
        raise ErrorDeHardware('no se obtuvo una lectura de seis angulos dentro del plazo; '
                              'respuestas=' + ', '.join(recibidos))

    def estado_movimiento(self, cancelado, limite):
        """Repite solo la consulta hasta tres veces; nunca presupone motor parado."""
        recibidos = []
        for intento in range(3):
            self.comprobar(cancelado)
            if time.monotonic() >= limite:
                raise ErrorDeHardware(
                    'plazo de movimiento agotado antes de consultar estado; '
                    'respuestas_previas=' + repr(recibidos))
            valor = self.mc.is_moving()
            recibidos.append(repr(valor))
            self.comprobar(cancelado)
            if time.monotonic() >= limite:
                raise ErrorDeHardware(
                    'plazo de movimiento agotado durante consulta de estado; '
                    'ultima_respuesta=' + repr(valor))
            if valor in (0, 1):
                return valor
            print('Lectura is_moving invalida: ' + repr(valor) +
                  '; intento ' + str(intento + 1) + '/3', flush=True)
            if intento < 2:
                time.sleep(0.15)
        raise ErrorDeHardware('estado de movimiento invalido; respuestas=' +
                              ', '.join(recibidos))

    def ejecutar_plan(self, trayectoria, cancelado):
        """Reproduce TODOS los puntos del plan de MoveIt2, con lectura real en cada uno.

        Los puntos intermedios se dan por alcanzados con una tolerancia más holgada que
        el punto final: parar en seco en cada punto multiplica el tiempo del pedido y,
        con la cola llena, dispara el tiempo límite.
        """
        puntos = [ordenar_articulaciones(trayectoria.joint_names, p.positions)
                  for p in trayectoria.points]
        if not puntos:
            raise ErrorDePedido('trayectoria vacia')
        tol_final = math.radians(self.c['tolerancia_articular_grados'])
        tol_media = math.radians(self.c['tolerancia_intermedia_grados'])
        q = self.leer(cancelado)
        if paso_articular(q, puntos[0]) > tol_media:
            raise ErrorDePedido('el brazo cambio de pose despues de planificar')
        maximo = math.radians(self.c['salto_maximo_plan_grados'])
        if any(paso_articular(a, b) > maximo for a, b in zip(puntos, puntos[1:])):
            raise ErrorDePedido('plan demasiado disperso para reproducir por puntos')
        ultimo = len(puntos) - 1
        for i, destino in enumerate(puntos[1:], start=1):
            self.comprobar(cancelado)
            final = i == ultimo
            tolerancia = tol_final if final else tol_media
            if self.mc.send_angles([math.degrees(v) for v in destino],
                                   self.c['velocidad_brazo']) == -1:
                raise ErrorDeHardware('el controlador rechazo el punto articular')
            limite = time.monotonic() + self.c['timeout_movimiento_s']
            ultimo_envio = time.monotonic()
            reintentos = 0
            detenido_desde = None
            time.sleep(0.05)
            estables = 0
            while True:
                self.comprobar(cancelado)
                try:
                    # Un intermedio solo requiere proximidad articular; no
                    # consultar is_moving para cada uno de los cientos de puntos.
                    moviendo = self.estado_movimiento(cancelado, limite) if final else None
                    q = self.leer(cancelado, limite)
                except ErrorDeHardware as exc:
                    if time.monotonic() >= limite:
                        error = math.degrees(paso_articular(q, destino))
                        raise ErrorDeHardware(
                            f'plazo agotado en punto {i}/{ultimo}; '
                            f'ultimo_error_grados={error:.2f}; '
                            f'pedidos_grados={[round(math.degrees(v), 2) for v in destino]}; '
                            f'ultima_lectura_grados={[round(math.degrees(v), 2) for v in q]}; '
                            f'causa={exc}') from exc
                    raise
                cerca = paso_articular(q, destino) <= tolerancia
                if final:
                    estables = estables + 1 if (cerca and moviendo == 0) else 0
                    if estables >= 2:
                        break
                elif cerca:
                    break           # intermedio: basta pasar cerca, sin frenar del todo
                if time.monotonic() >= limite:
                    pedidos = [round(math.degrees(v), 2) for v in destino]
                    leidos = [round(math.degrees(v), 2) for v in q]
                    errores = [round(math.degrees(abs(a - b)), 2)
                               for a, b in zip(q, destino)]
                    peor = max(range(len(errores)), key=errores.__getitem__) + 1
                    raise ErrorDeHardware(
                        f'el brazo no alcanzo el punto {i}/{ultimo} del plan '
                        f'(error {math.degrees(paso_articular(q, destino)):.1f} grados); '
                        f'articulacion_mayor_error={peor}; '
                        f'pedidos_grados={pedidos}; leidos_grados={leidos}; '
                        f'errores_grados={errores}; motor_moviendo={moviendo}; '
                        f'tolerancia_grados={math.degrees(tolerancia):.2f}; '
                        f'reintentos_final={reintentos}')
                # Un solo reenvio del MISMO destino, solo cerca y detenido.
                # No prolonga el plazo ni cambia la tolerancia de llegada.
                error = paso_articular(q, destino)
                ahora = time.monotonic()
                apto = (final and moviendo == 0 and
                        tol_final < error <= min(tol_media, math.radians(3.0)))
                if apto:
                    if detenido_desde is None:
                        detenido_desde = ahora
                else:
                    detenido_desde = None
                if (apto and reintentos < 1 and
                        ahora - detenido_desde >= 0.5 and
                        ahora - ultimo_envio >= 1.0):
                    self.comprobar(cancelado)
                    if self.mc.send_angles([math.degrees(v) for v in destino],
                                           self.c['velocidad_brazo']) == -1:
                        raise ErrorDeHardware('el controlador rechazo el reintento final')
                    reintentos += 1
                    ultimo_envio = time.monotonic()
                    detenido_desde = None
                    estables = 0
                time.sleep(0.05 if not final else 0.1)
        return self.leer(cancelado)

    def pinza(self, valor, cancelado):
        self.comprobar(cancelado)
        if self.mc.set_gripper_value(valor, self.c['velocidad_pinza']) == -1:
            raise ErrorDeHardware('el controlador rechazo el comando de pinza')
        time.sleep(0.5)
        limite = time.monotonic() + self.c['timeout_pinza_s']
        while True:
            self.comprobar(cancelado)
            estado = self.mc.is_gripper_moving()
            if estado == 0:
                return   # Motor detenido NO significa que haya agarrado un cubo.
            if estado != 1:
                raise ErrorDeHardware('estado de pinza invalido')
            if time.monotonic() >= limite:
                raise ErrorDeHardware('la pinza no termino el movimiento')
            time.sleep(0.1)

    def detener(self):
        if self.mc is not None:
            if self.mc.stop() == -1:
                raise ErrorDeHardware('el controlador no confirmo la parada')
            # No soltar la pinza automáticamente: podría contener el objeto.

    def close(self):
        if self.mc is not None:
            try:
                self.mc.close()
            finally:
                self.mc = None
        if self.cerrojo is not None:
            try:
                self.cerrojo.close()
            finally:
                self.cerrojo = None


class SecuenciaFisica:
    """Una recogida completa atendida como UN pedido del broker (la cola no se libera)."""

    def __init__(self, config, planificador, brazo, vision):
        self.c = config
        self.plan = planificador
        self.brazo = brazo
        self.vision = vision

    def ejecutar(self, color, cancelado, feedback, carpeta, registro):
        c = self.c
        etapas, tiempos = registro['stages'], registro['stage_time_s']

        def etapa(nombre, accion):
            if cancelado():
                raise Cancelado('cancelado antes de ' + nombre)
            feedback(nombre)
            inicio = time.monotonic()
            try:
                return accion()
            finally:
                etapas.append(nombre)
                tiempos.append(time.monotonic() - inicio)

        def mover(nombre, referencia, altura=0.0):
            actual = self.brazo.leer()
            trayectoria, subetapas, duraciones = etapa('PLAN_' + nombre, lambda: (
                self.plan.planificar_referencia(referencia, actual, cancelado,
                                                lambda m: feedback(nombre + ':' + m), altura)))
            # Subtiempos anidados: no sumarlos otra vez a las etapas principales.
            registro.setdefault('planes', []).append(
                dict(segmento=nombre, stages=subetapas, stage_time_s=duraciones))
            return etapa('MOVER_' + nombre,
                         lambda: self.brazo.ejecutar_plan(trayectoria, cancelado))

        escaneo = radianes(c['escaneo_grados'])
        deposito = radianes(c['_deposito'][color])
        mover('ESCANEO', escaneo)
        observacion = etapa('DETECTAR_COLOR',
                           lambda: self.vision.observar(color, cancelado, carpeta, 'color'))
        registro['deteccion_color'] = observacion
        if not observacion['detectado']:
            raise ErrorDePedido(observacion.get('motivo', 'no se detecto el color ' + color))
        posicion = observacion.get('posicion')
        if posicion not in c['posiciones_recogida']:
            raise ErrorDePedido('la camara no devolvio una posicion de recogida valida')
        recogida = radianes(c['posiciones_recogida'][posicion]['grados'])
        registro['posicion_recogida'] = posicion
        registro['q_recogida_seleccionada_rad'] = list(recogida)
        feedback('LOCALIZADO_' + color.upper() + '_EN_' + posicion.upper())

        etapa('ABRIR_PINZA', lambda: self.brazo.pinza(c['pinza_abierta'], cancelado))
        medida_agarre = mover('AGARRE', recogida)
        registro['q_agarre_rad'] = medida_agarre
        registro['xyz_agarre_solicitada_mm'] = list(fk(recogida))
        registro['xyz_agarre_alcanzada_mm'] = list(fk(medida_agarre))
        registro['error_agarre_mm'] = math.dist(registro['xyz_agarre_solicitada_mm'],
                                             registro['xyz_agarre_alcanzada_mm'])
        registro['pinza_puede_contener_cubo'] = True
        etapa('CERRAR_PINZA', lambda: self.brazo.pinza(c['pinza_cerrada'], cancelado))
        mover('LEVANTAR_A_ESCANEO', escaneo)
        medida = mover('DEPOSITO', deposito)
        registro['q_solicitada_rad'] = deposito
        registro['q_alcanzada_rad'] = medida
        registro['xyz_solicitada_mm'] = list(fk(deposito))
        registro['xyz_alcanzada_mm'] = list(fk(medida))
        registro['position_error_mm'] = math.dist(registro['xyz_solicitada_mm'],
                                                 registro['xyz_alcanzada_mm'])
        etapa('SOLTAR', lambda: self.brazo.pinza(c['pinza_abierta'], cancelado))
        registro['pinza_puede_contener_cubo'] = False
        mover('REGRESAR_A_ESCANEO', escaneo)
        # Se registra el ciclo ejecutado; no se afirma haber observado el depósito.
        registro['physical_verified'] = False
        registro['interpretacion_error'] = 'Desviacion articular expresada por FK RB2; no mide el cubo.'
        return etapas, tiempos


# ==========================================================================
# 8. Secuencia simulada: sin ROS real, sin cámara, sin IK ni MoveIt2.
# ==========================================================================

ETAPAS_SIMULADAS = ('OBSERVAR_SIMULADO', 'LOCALIZAR_SIMULADO', 'IK_SIMULADA',
                    'PLANIFICAR_SIMULADO', 'APROXIMAR_SIMULADO', 'CERRAR_PINZA_SIMULADO',
                    'LEVANTAR_SIMULADO', 'TRASLADAR_SIMULADO', 'ABRIR_PINZA_SIMULADO',
                    'RETIRAR_SIMULADO')


class SecuenciaSimulada:
    def __init__(self, duracion_etapa_s=0.05):
        if not math.isfinite(duracion_etapa_s) or duracion_etapa_s < 0:
            raise ValueError('duracion de etapa debe ser finita y no negativa')
        self.duracion = duracion_etapa_s

    def ejecutar(self, cancelado, feedback):
        etapas, tiempos = [], []
        for etapa in ETAPAS_SIMULADAS:
            if cancelado():
                raise Cancelado('cancelado antes de ' + etapa)
            feedback(etapa)
            inicio = time.perf_counter()
            fin = inicio + self.duracion
            while time.perf_counter() < fin:
                if cancelado():
                    raise Cancelado('cancelado durante ' + etapa)
                time.sleep(min(0.01, max(0, fin - time.perf_counter())))
            etapas.append(etapa)
            tiempos.append(time.perf_counter() - inicio)
        if cancelado():
            raise Cancelado('cancelado al terminar la simulacion')
        return etapas, tiempos


def validar_pedido(req, inventario, zonas, permitir_respaldo=False, acciones=('recoger',)):
    """Filtro de la decisión del modelo ANTES de encolar (requisito 3 de la Pregunta 2)."""
    if not req.permitido:
        return False, 'decision no permitida: rechazada antes de encolar'
    if req.accion not in acciones:
        return False, f'accion "{req.accion}" no admitida (se admiten: {", ".join(acciones)})'
    if req.fuente not in ('LAYA', 'respaldo', 'LOCAL_SIN_LAYA'):
        return False, 'fuente desconocida'
    if req.degradada != (req.fuente in ('respaldo', 'LOCAL_SIN_LAYA')):
        return False, 'fuente y bandera degradada inconsistentes'
    if req.degradada and not permitir_respaldo:
        return False, 'respuesta degradada y el respaldo no esta habilitado para esta prueba'
    if f'{req.objeto}:{req.color}' not in inventario:
        return False, 'objeto/color no incluido en el inventario configurado'
    if req.zona not in zonas:
        return False, 'zona desconocida'
    return True, ''


# ==========================================================================
# 9. Evidencia: CSV y detalle JSON de intentos reales.
#    Las simulaciones nunca entran en la tasa de éxito.
# ==========================================================================

CAMPOS_EVIDENCIA = [
    'goal_id', 'fecha', 'cliente', 'accion', 'color', 'zona', 'prioridad', 'fuente',
    'degradada', 'success', 'physical_verified', 'position_error_mm', 'error_agarre_mm',
    'wait_time_s', 'exec_time_s', 'message', 'q_solicitada_rad', 'q_alcanzada_rad',
    'xyz_solicitada_mm', 'xyz_alcanzada_mm',
]


def guardar_evidencia(carpeta, registro):
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    detalle = carpeta / registro['goal_id']
    detalle.mkdir(exist_ok=True)
    (detalle / 'intento.json').write_text(
        json.dumps(registro, ensure_ascii=False, indent=2), encoding='utf-8')
    archivo = carpeta / 'intentos.csv'
    nuevo = not archivo.exists()
    with archivo.open('a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_EVIDENCIA)
        if nuevo:
            w.writeheader()
        w.writerow({k: json.dumps(registro[k]) if isinstance(registro.get(k), list)
                    else registro.get(k, '') for k in CAMPOS_EVIDENCIA})


# ==========================================================================
# 10. Nodo ROS 2
# ==========================================================================

class ArmBroker(Node):

    def __init__(self):
        super().__init__('arm_broker')

        # ----- parámetros (se cambian con --ros-args -p nombre:=valor; usa decimales: 2.0, no 2)
        self.declare_parameter('politica', 'fifo')
        # SEGURO POR DEFECTO: hasta habilitar explícitamente, NO manda a las articulaciones.
        self.declare_parameter('publicar_joint_states', False)
        self.declare_parameter('tau_envejecimiento_s', 8.0)
        self.declare_parameter('cola_max', 20)
        self.declare_parameter('paso_max_rad', 1.2)
        self.declare_parameter('duracion_movimiento_s', 3.0)
        self.declare_parameter('pasos_interpolacion', 10)
        # Pose en la que SE SUPONE que está el brazo al arrancar el broker (la base = ceros).
        self.declare_parameter('q_inicial_rad', [0.0] * 6)
        # Archivo donde se anota cada rechazo con su motivo ('' = no escribir archivo).
        self.declare_parameter('archivo_rechazos', 'registro_rechazos.csv')
        # ----- Pregunta 2
        self.declare_parameter('habilitar_pick_place_simulado', False)
        self.declare_parameter('habilitar_planificacion_pick_place', False)
        self.declare_parameter('habilitar_pick_place_fisico', False)
        self.declare_parameter('config_item2', '')
        self.declare_parameter('evidencias_item2', 'evidencias/item2')
        self.declare_parameter('permitir_respaldo_pick_place', False)
        self.declare_parameter('inventario_pick_place', [''])
        self.declare_parameter('zonas_pick_place', ['deposito'])
        self.declare_parameter('acciones_pick_place', ['recoger', 'colocar'])
        self.declare_parameter('duracion_etapa_simulada_s', 0.05)
        self.declare_parameter('objetivos_planificacion_json', '{}')
        self.declare_parameter('usar_semilla_configurada', False)
        self.declare_parameter('semilla_planificacion_rad', [0.0] * 6)
        self.declare_parameter('moveit_grupo', 'arm_group')
        self.declare_parameter('moveit_enlace', '6_Link')
        self.declare_parameter('moveit_marco', 'base_link')
        self.declare_parameter('moveit_timeout_s', 8.0)

        aviso = _verificar_fk_externa()
        if aviso:
            self.get_logger().warn('COHERENCIA FK: ' + aviso)

        nombre = self.get_parameter('politica').value
        if nombre not in POLITICAS:
            raise RuntimeError(f'política desconocida: {nombre}. Hay {list(POLITICAS)}')
        clase = POLITICAS[nombre]
        if nombre == 'prioridad':
            self.politica = clase(self.get_parameter('tau_envejecimiento_s').value)
        else:
            self.politica = clase()

        self.publicar_joint_states = bool(self.get_parameter('publicar_joint_states').value)
        self.solo_plan = bool(self.get_parameter('habilitar_planificacion_pick_place').value)
        self.pick_simulado = bool(self.get_parameter('habilitar_pick_place_simulado').value)
        self.pick_fisico = bool(self.get_parameter('habilitar_pick_place_fisico').value)
        if sum((self.solo_plan, self.pick_simulado, self.pick_fisico)) > 1:
            raise RuntimeError('elige UN modo de PickPlace: simulado, planificacion o fisico')
        if (self.solo_plan or self.pick_simulado or self.pick_fisico) and self.publicar_joint_states:
            raise RuntimeError('PickPlace requiere publicar_joint_states=false')

        self.fallo_fisico = ''
        self.montaje = None
        if self.pick_fisico:
            self.montaje = cargar_montaje(self.get_parameter('config_item2').value, fisico=True,
                                          avisar=lambda m: self.get_logger().warn('MONTAJE: ' + m))

        self.permitir_respaldo = bool(self.get_parameter('permitir_respaldo_pick_place').value)
        self.inventario_pick = set(self.get_parameter('inventario_pick_place').value)
        self.zonas_pick = set(self.get_parameter('zonas_pick_place').value)
        self.acciones_pick = tuple(self.get_parameter('acciones_pick_place').value)
        self.secuencia = SecuenciaSimulada(
            float(self.get_parameter('duracion_etapa_simulada_s').value))
        self.cola_max = int(self.get_parameter('cola_max').value)
        self.paso_max = float(self.get_parameter('paso_max_rad').value)
        self.duracion = float(self.get_parameter('duracion_movimiento_s').value)
        self.pasos = max(1, int(self.get_parameter('pasos_interpolacion').value))
        self.archivo_rechazos = str(self.get_parameter('archivo_rechazos').value)

        # ----- grupos de callbacks
        # Reentrante: varios callbacks a la vez (aceptar goals MIENTRAS otro se ejecuta).
        # Exclusivo: sus callbacks corren de uno en uno (el temporizador de la cola).
        # OJO: la exclusión mutua del BRAZO no la dan los grupos, la da el worker único.
        self.grupo_entrada = ReentrantCallbackGroup()
        self.grupo_worker = MutuallyExclusiveCallbackGroup()

        # ----- estado compartido: TODO acceso a estas variables va bajo self.lock
        self.lock = threading.Lock()
        self._lock_archivo = threading.Lock()
        self.reservados = 0             # aceptados aún no encolados
        self.pendientes = []            # la sala de espera (lista de Pedido)
        self.por_goal_id = {}           # índice goal_id -> Pedido, para execute_callback
        self.ejecutando = None          # el Pedido que mueve el brazo AHORA (o None)
        q0 = list(self.get_parameter('q_inicial_rad').value)
        if len(q0) != 6:
            self.get_logger().warn('q_inicial_rad debe tener 6 valores; uso ceros')
            q0 = [0.0] * 6
        self.q_actual = q0
        self.n_aceptados = 0
        self.n_rechazados = 0
        self.n_completados = 0
        self._parar = threading.Event()

        self.pub_joint = self.create_publisher(JointState, '/joint_states', 10)
        self.pub_cola = self.create_publisher(QueueState, '/arm/queue_state', 10)
        self.pub_medida = (self.create_publisher(JointState, '/arm/measured_joint_states', 10)
                           if self.pick_fisico else None)

        self.servidor = ActionServer(
            self, MoveArm, 'move_arm',
            goal_callback=self.goal_callback,
            handle_accepted_callback=self.handle_accepted_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=self.grupo_entrada,
        )
        self.servidor_pick = ActionServer(
            self, PickPlace, 'pick_place',
            goal_callback=self.pick_goal_callback,
            handle_accepted_callback=self.handle_accepted_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_pick_callback,
            callback_group=self.grupo_entrada,
        )

        # /arm/queue_state a 5 Hz
        self.create_timer(0.2, self.publicar_estado_cola, callback_group=self.grupo_worker)

        self.planificador = None
        self.estado_plan_q = None
        self.estado_plan_t = 0.0
        self.objetivos_plan = {}
        if self.solo_plan:
            self.objetivos_plan = cargar_objetivos(
                self.get_parameter('objetivos_planificacion_json').value)
            timeout = float(self.get_parameter('moveit_timeout_s').value)
            if not math.isfinite(timeout) or not 0.1 <= timeout <= 30:
                raise ValueError('moveit_timeout_s debe estar entre 0.1 y 30')
            self.semilla_manual = bool(self.get_parameter('usar_semilla_configurada').value)
            self.semilla_plan = seis_finitos(
                self.get_parameter('semilla_planificacion_rad').value, 'semilla')
            self.planificador = self._crear_planificador(timeout)
            self.sub_estado_plan = self.create_subscription(
                JointState, '/joint_states', self.recibir_estado_plan, 10,
                callback_group=self.grupo_entrada)
            self.get_logger().warn('SOLO PLANIFICACION: IK y trayectoria; nunca ejecucion. '
                                   'Con semilla manual el estado inicial es hipotetico.')
        if self.pick_fisico:
            self.planificador = self._crear_planificador(
                float(self.get_parameter('moveit_timeout_s').value),
                self.montaje.get('tolerancia_modelo_mm', 10.0))
            self.get_logger().warn(
                'FISICO: comandos por pymycobot SOLO en el hilo worker; detén notebooks y '
                'drivers seriales anteriores. /arm/measured_joint_states es LECTURA.')

        # El trabajador único
        self.worker = threading.Thread(target=self._worker, daemon=True)
        self.worker.start()

        modo = ('fisico' if self.pick_fisico else 'planificacion' if self.solo_plan
                else 'pick simulado' if self.pick_simulado else 'solo MoveArm')
        self.get_logger().info(
            f'arm_broker listo · política={self.politica.nombre} · modo={modo} · '
            f'cola_max={self.cola_max} · paso_max={self.paso_max:.2f} rad · '
            f'publicacion a /joint_states habilitada={self.publicar_joint_states}')
        if not self.publicar_joint_states and not self.pick_fisico:
            self.get_logger().warn('MODO SIMULADO: no se publican ordenes /joint_states; '
                                   'no es evidencia de movimiento real')

    def _crear_planificador(self, timeout, tolerancia_modelo_mm=10.0):
        return Planificador(self,
                            self.get_parameter('moveit_grupo').value,
                            self.get_parameter('moveit_enlace').value,
                            self.get_parameter('moveit_marco').value,
                            timeout, tolerancia_modelo_mm)

    # ========================= IMPLEMENTAR · ítem 2 ==========================
    def goal_callback(self, goal_request):
        """EL PORTERO. Admisión barata e inmediata: acepta o rechaza, NUNCA ejecuta.

        Los filtros van del más barato al más caro. Cada rechazo lleva un motivo legible
        con los números que lo causaron (lo exige la rúbrica).
        """
        if self.pick_fisico:
            return self._rechazar(goal_request.client_id,
                                  'MoveArm deshabilitado durante PickPlace fisico; '
                                  'usa la accion /pick_place')
        q = list(goal_request.joint_positions)
        cliente = goal_request.client_id or '?'

        # 1) Límites articulares (comparación directa, no necesita FK)
        ok, motivo = dentro_de_limites(q)
        if not ok:
            return self._rechazar(cliente, f'límites articulares: {motivo}', q)

        # 2) Workspace (aquí entra la FK: distancia a la base y z >= 0)
        ok, motivo = dentro_del_workspace(q)
        if not ok:
            return self._rechazar(cliente, f'workspace: {motivo}', q)

        # 3) Paso articular desde la pose actual del brazo
        with self.lock:
            desde = list(self.q_actual)
        paso = paso_articular(desde, q)
        if paso > self.paso_max:
            return self._rechazar(
                cliente, f'paso articular excesivo: {paso:.2f} rad, máximo {self.paso_max:.2f}', q)

        # 4) Reserva atómica: cuenta también los aceptados que aún no se encolaron.
        if not self._reservar():
            return self._rechazar(cliente, f'cola llena (maximo {self.cola_max})', q)
        x, y, z = fk(q)
        self.get_logger().info(f'ACEPTADO  {cliente}  ->  ({x:.0f}, {y:.0f}, {z:.0f}) mm')
        return GoalResponse.ACCEPT

    def pick_goal_callback(self, req):
        """EL PORTERO de PickPlace: aquí se rechaza la orden NO permitida, antes de la cola."""
        if self.fallo_fisico:
            return self._rechazar(req.client_id,
                                  'brazo enclavado por un fallo de hardware anterior ('
                                  + self.fallo_fisico + '); revisa el montaje y reinicia el broker')
        if not (self.pick_simulado or self.solo_plan or self.pick_fisico):
            return self._rechazar(req.client_id, 'PickPlace deshabilitado en este broker')
        ok, motivo = validar_pedido(req, self.inventario_pick, self.zonas_pick,
                                    self.permitir_respaldo, self.acciones_pick)
        if not ok:
            return self._rechazar(req.client_id, motivo)
        if self.pick_fisico and (req.objeto != 'cubo'
                                 or req.color not in COLORES
                                 or req.zona != 'deposito'):
            return self._rechazar(req.client_id, 'pedido fuera de las posiciones fijas '
                                                 'configuradas para este montaje')
        if self.solo_plan:
            clave = f'{req.objeto}:{req.color}@{req.zona}'
            if clave not in self.objetivos_plan:
                return self._rechazar(req.client_id, 'falta pose objetivo para ' + clave)
        if not self._reservar():
            return self._rechazar(req.client_id, f'cola llena (maximo {self.cola_max})')
        self.get_logger().info(
            f'ACEPTADO  {req.client_id}  ->  {req.accion} {req.objeto} {req.color} '
            f'-> {req.zona}  (prioridad {req.priority}, fuente {req.fuente})')
        return GoalResponse.ACCEPT

    def _reservar(self):
        with self.lock:
            if len(self.pendientes) + self.reservados >= self.cola_max:
                return False
            self.reservados += 1
            self.n_aceptados += 1
            return True

    def _rechazar(self, cliente, motivo, q=None):
        """Cuenta el rechazo, lo escribe en el log y en el CSV de rechazos."""
        with self.lock:
            self.n_rechazados += 1
        self.get_logger().warn(f'RECHAZADO {cliente or "?"}: {motivo}')
        self._anotar_rechazo(cliente, motivo, q)
        return GoalResponse.REJECT

    def _anotar_rechazo(self, cliente, motivo, q):
        if not self.archivo_rechazos:
            return
        try:
            with self._lock_archivo:
                ruta = Path(self.archivo_rechazos)
                if ruta.parent and not ruta.parent.exists():
                    ruta.parent.mkdir(parents=True, exist_ok=True)
                nuevo = not ruta.exists()
                with ruta.open('a', newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    if nuevo:
                        w.writerow(['hora', 'cliente', 'motivo', 'q_pedida_rad'])
                    w.writerow([time.strftime('%Y-%m-%dT%H:%M:%S'), cliente, motivo,
                                '' if q is None else ' '.join(f'{v:.3f}' for v in q)])
        except OSError as e:   # el archivo es un extra: nunca tumba la admisión
            self.get_logger().warn(f'no pude escribir {self.archivo_rechazos}: {e}')

    def handle_accepted_callback(self, goal_handle):
        """LA SALA DE ESPERA. Solo encola: aquí NO se ejecuta nada ni se publica nada.

        Corre en el grupo reentrante (varios clientes a la vez), por eso toda escritura a
        self.pendientes va bajo self.lock.
        """
        pedido = Pedido(goal_handle,
                        goal_handle.request.client_id,
                        goal_handle.request.priority,
                        getattr(goal_handle.request, 'joint_positions', []))
        pedido.tipo_pick = hasattr(goal_handle.request, 'objeto')
        with self.lock:
            self.reservados -= 1
            self.pendientes.append(pedido)
            self.por_goal_id[pedido.goal_id] = pedido
            posicion = len(self.pendientes)
        self.get_logger().info(
            f'ENCOLADO  {pedido.client_id}  posición {posicion}  (no se ejecuta aquí)')

    def _worker(self):
        """EL TRABAJADOR ÚNICO. Un solo hilo decide a quién le toca y atiende de a uno."""
        while not self._parar.is_set():
            pedido = None
            with self.lock:
                # Solo se saca otro pedido si nadie se está ejecutando (1.ª defensa)
                if self.ejecutando is None and self.pendientes:
                    idx = self.politica.siguiente(self.pendientes)   # la política decide
                    if idx is not None:
                        pedido = self.pendientes.pop(idx)
                        # Se ejecuta incluso cancelado, para devolver resultado al cliente.
                        self.ejecutando = pedido
                        pedido.t_inicio_ejec = time.time()

            if pedido is None:
                time.sleep(0.02)                  # nada que hacer: no quemes CPU
                continue

            try:
                pedido.goal_handle.execute()      # dispara execute_callback en otro hilo
            except Exception as e:
                self.get_logger().error(f'execute() falló: {e}')
                try:
                    pedido.goal_handle.abort()
                except Exception:
                    pass
                pedido.fin.set()

            # EXCLUSIÓN MUTUA: no se saca otro pedido hasta que este termine.
            while not pedido.fin.wait(0.02):
                # El callback de la acción encarga el trabajo físico a ESTE hilo: toda
                # llamada al puerto serie, incluida la parada, ocurre en el worker.
                trabajo = pedido.trabajo_fisico
                if trabajo is not None:
                    pedido.trabajo_fisico = None
                    trabajo()
                if self._parar.is_set() and not pedido.esperando_fisico:
                    break

            with self.lock:
                self.ejecutando = None
                self.por_goal_id.pop(pedido.goal_id, None)
                # solo cuenta como completado el que terminó con éxito
                if pedido.resultado is not None and pedido.resultado.success:
                    self.n_completados += 1
            self.politica.atendido(pedido)

    def execute_callback(self, goal_handle):
        """Ejecuta UN pedido MoveArm (lo llama el worker, nunca handle_accepted).

        Interpola desde q_actual hasta el destino en self.pasos pasos y publica cada paso
        con mover(), el ÚNICO punto del programa que publica en /joint_states.
        """
        gid = bytes(goal_handle.goal_id.uuid).hex()[:12]
        with self.lock:
            pedido = self.por_goal_id.get(gid)
        resultado = MoveArm.Result()

        if pedido is None:
            goal_handle.abort()
            resultado.success = False
            resultado.message = 'pedido desconocido'
            return resultado

        try:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                resultado.success = False
                resultado.message = 'cancelado en cola'
                resultado.wait_time_s = float(pedido.espera_s)
                return resultado
            destino = list(pedido.joint_positions)
            with self.lock:
                desde = list(self.q_actual)
            if paso_articular(desde, destino) > self.paso_max:
                raise ValueError('paso articular excesivo desde la pose al desencolar')
            t0 = time.time()
            dt = self.duracion / self.pasos       # p. ej. 3.0 s / 10 pasos = 0.3 s por paso
            self.get_logger().info(
                f'EJECUTANDO {pedido.client_id}  goal={pedido.goal_id}  '
                f'espera={pedido.espera_s:.2f}s')

            for paso in range(1, self.pasos + 1):
                if goal_handle.is_cancel_requested or self._parar.is_set():
                    if goal_handle.is_cancel_requested:
                        goal_handle.canceled()
                    else:
                        goal_handle.abort()
                    resultado.success = False
                    resultado.message = f'cancelado en el paso {paso}/{self.pasos}'
                    resultado.wait_time_s = pedido.espera_s
                    resultado.exec_time_s = time.time() - t0
                    return resultado

                frac = paso / self.pasos          # 0.1, 0.2, ... 1.0
                q = [a + (b - a) * frac for a, b in zip(desde, destino)]
                self.mover(q)                     # ← única publicación en /joint_states

                fb = MoveArm.Feedback()
                fb.state = 'EXECUTING'
                fb.queue_position = 0
                fb.elapsed_s = time.time() - t0
                goal_handle.publish_feedback(fb)
                time.sleep(dt)

            goal_handle.succeed()
            x, y, z = fk(destino)
            resultado.success = True
            resultado.message = (
                ('EJECUCION SIMULADA sin enviar al brazo; ' if not self.publicar_joint_states
                 else '') + f'pose calculada ({x:.0f}, {y:.0f}, {z:.0f}) mm')
            resultado.wait_time_s = pedido.espera_s
            resultado.exec_time_s = time.time() - t0
            self.get_logger().info(
                f'COMPLETADO {pedido.client_id}  goal={pedido.goal_id}  '
                f'espera={resultado.wait_time_s:.2f}s ejec={resultado.exec_time_s:.2f}s')
            return resultado
        except Exception as e:                    # un fallo no debe dejar el brazo bloqueado
            self.get_logger().error(f'falló la ejecución de {pedido.client_id}: {e}')
            try:
                goal_handle.abort()
            except Exception:
                pass
            resultado.success = False
            resultado.message = f'error: {e}'
            return resultado
        finally:
            # PASE LO QUE PASE: si no se levanta la bandera, el worker espera para siempre
            pedido.resultado = resultado
            pedido.fin.set()
    # =========================================================================

    def recibir_estado_plan(self, msg):
        try:
            q = ordenar_articulaciones(msg.name, msg.position)
        except ValueError:
            return
        with self.lock:
            self.estado_plan_q = q
            self.estado_plan_t = time.monotonic()

    def execute_pick_callback(self, goal_handle):
        """Ejecuta UN pedido PickPlace: simulado, solo planificación o físico."""
        gid = bytes(goal_handle.goal_id.uuid).hex()[:12]
        with self.lock:
            pedido = self.por_goal_id.get(gid)
        resultado = PickPlace.Result()
        resultado.simulated = not (self.solo_plan or self.pick_fisico)
        resultado.planning_only = self.solo_plan
        resultado.physical_verified = False
        resultado.position_error_mm = -1.0        # sin medición física
        inicio = time.perf_counter()
        registro = None
        if pedido is None:
            goal_handle.abort()
            resultado.success = False
            resultado.message = 'pedido desconocido'
            return resultado

        try:
            def feedback(etapa):
                fb = PickPlace.Feedback()
                fb.state = etapa
                fb.queue_position = 0
                fb.elapsed_s = time.perf_counter() - inicio
                goal_handle.publish_feedback(fb)

            def cancelado():
                return goal_handle.is_cancel_requested or self._parar.is_set()

            if cancelado():
                raise Cancelado('cancelado antes de ejecutar')

            if self.pick_fisico:
                if self.fallo_fisico:
                    raise ErrorDePedido('ejecucion detenida por un fallo anterior: '
                                        + self.fallo_fisico)
                req = goal_handle.request
                registro = dict(
                    goal_id=gid, fecha=time.strftime('%Y-%m-%dT%H:%M:%S'),
                    cliente=req.client_id, accion=req.accion, color=req.color, zona=req.zona,
                    prioridad=req.priority, fuente=req.fuente, degradada=req.degradada,
                    stages=[], stage_time_s=[], physical_verified=False,
                    position_error_mm=-1.0, error_agarre_mm=-1.0)
                self._ejecutar_en_worker(pedido, lambda: self._recoger_fisico(
                    req.color, cancelado, feedback, registro))
                etapas, tiempos = registro['stages'], registro['stage_time_s']
                resultado.physical_verified = registro['physical_verified']
                resultado.position_error_mm = registro['position_error_mm']
            elif self.solo_plan:
                req = goal_handle.request
                objetivo = self.objetivos_plan[f'{req.objeto}:{req.color}@{req.zona}']
                if self.semilla_manual:
                    semilla = list(self.semilla_plan)
                else:
                    with self.lock:
                        if self.estado_plan_q is None or time.monotonic() - self.estado_plan_t > 2.0:
                            raise ErrorDePedido('no hay /joint_states reciente con las seis '
                                                'articulaciones')
                        semilla = list(self.estado_plan_q)
                etapas, tiempos = self.planificador.calcular(objetivo, semilla, cancelado, feedback)
            else:
                etapas, tiempos = self.secuencia.ejecutar(cancelado, feedback)

            resultado.stages = list(etapas)
            resultado.stage_time_s = list(tiempos)
            resultado.success = True
            resultado.message = (
                'SOLO PLANIFICACION: IK y trayectoria calculadas, NO EJECUTADAS; sin '
                'percepcion ni agarre; objetivo del enlace MoveIt configurado'
                if self.solo_plan else
                'CICLO COMPLETADO: recogida y deposito; sin verificacion visual final' if self.pick_fisico else
                'SECUENCIA SIMULADA; sin camara, IK real, MoveIt2 ni comandos fisicos')
            goal_handle.succeed()
        except Cancelado as exc:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
            else:
                goal_handle.abort()
            resultado.success = False
            resultado.message = str(exc)
        except ErrorDePedido as exc:
            # El intento falla; el brazo queda utilizable y la cola sigue.
            goal_handle.abort()
            resultado.success = False
            resultado.message = 'intento fallido: ' + str(exc)
            self.get_logger().warn(f'INTENTO FALLIDO {pedido.client_id}: {exc}')
        except ErrorDeHardware as exc:
            self.fallo_fisico = str(exc)
            goal_handle.abort()
            resultado.success = False
            resultado.message = 'FALLO DE HARDWARE (broker enclavado): ' + str(exc)
            self.get_logger().error('FALLO DE HARDWARE, no se admiten mas pedidos fisicos: '
                                    + str(exc))
        except Exception as exc:
            self.fallo_fisico = str(exc) if self.pick_fisico else ''
            goal_handle.abort()
            resultado.success = False
            resultado.message = f'error de secuencia: {exc}'
            self.get_logger().error(f'error de secuencia: {exc}')
        finally:
            resultado.wait_time_s = float(pedido.espera_s)
            resultado.exec_time_s = time.perf_counter() - inicio
            if registro is not None:
                resultado.stages = list(registro['stages'])
                resultado.stage_time_s = list(registro['stage_time_s'])
                resultado.position_error_mm = registro['position_error_mm']
                resultado.physical_verified = registro['physical_verified']
                registro.update(success=resultado.success, message=resultado.message,
                                wait_time_s=resultado.wait_time_s,
                                exec_time_s=resultado.exec_time_s)
                try:
                    guardar_evidencia(self.get_parameter('evidencias_item2').value, registro)
                except Exception as exc:
                    # Sin evidencia no hay intento válido: esto sí detiene la sesión.
                    self.fallo_fisico = 'no se pudo guardar la evidencia: ' + str(exc)
                    self.get_logger().error(self.fallo_fisico)
                    resultado.message += '; ERROR AL GUARDAR EVIDENCIA: ' + str(exc)
            pedido.resultado = resultado
            pedido.fin.set()
        return resultado

    def _ejecutar_en_worker(self, pedido, funcion):
        """Encarga la secuencia física al hilo worker y espera aquí su resultado."""
        listo = threading.Event()
        errores = []

        def trabajo():
            try:
                funcion()
            except BaseException as exc:
                errores.append(exc)
            finally:
                listo.set()

        pedido.esperando_fisico = True
        pedido.trabajo_fisico = trabajo
        try:
            while not listo.wait(0.1):
                if not self.worker.is_alive():
                    raise ErrorDeHardware('el worker termino antes de completar la secuencia')
            if errores:
                raise errores[0]
        finally:
            pedido.esperando_fisico = False

    def _recoger_fisico(self, color, cancelado, feedback, registro):
        brazo = None
        try:
            if cancelado():
                raise Cancelado('cancelado antes de abrir el puerto')
            brazo = BrazoSerial(self.montaje, self._publicar_medida)
            secuencia = SecuenciaFisica(self.montaje, self.planificador, brazo,
                                        VisionFija(self.montaje))
            carpeta = Path(self.get_parameter('evidencias_item2').value) / registro['goal_id']
            secuencia.ejecutar(color, cancelado, feedback, carpeta, registro)
        except (ErrorDePedido, Cancelado) as exc:
            # El brazo quedó en una pose conocida: se intenta dejarlo quieto y se sigue.
            if brazo is not None:
                try:
                    brazo.detener()
                except Exception as parada_exc:
                    raise ErrorDeHardware('parada sin confirmar: ' + str(parada_exc)) from parada_exc
            if registro.get('pinza_puede_contener_cubo'):
                raise ErrorDeHardware('ciclo interrumpido con un cubo posiblemente sujeto: ' + str(exc)) from exc
            raise
        except BaseException as exc:
            if brazo is not None:
                try:
                    brazo.detener()
                except Exception as exc2:
                    self.get_logger().error('parada serial sin confirmar: ' + str(exc2))
            if isinstance(exc, ErrorDeHardware):
                raise
            raise ErrorDeHardware(str(exc)) from exc
        finally:
            if brazo is not None:
                try:
                    brazo.close()
                except Exception as exc:
                    self.fallo_fisico = 'el puerto no se cerro limpio: ' + str(exc)
                    self.get_logger().error(self.fallo_fisico)

    def _publicar_medida(self, q):
        if threading.current_thread() is not self.worker:
            raise ErrorDeHardware('lectura fisica fuera del worker')
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.get_parameter('moveit_marco').value
        msg.name = list(JOINT_NAMES)
        msg.position = list(q)
        self.pub_medida.publish(msg)
        with self.lock:
            self.q_actual = list(q)

    def cancel_callback(self, goal_handle):
        return CancelResponse.ACCEPT

    # ----------------------------------------------------------- publicar
    def mover(self, q):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.name = JOINT_NAMES
        msg.position = [float(v) for v in q]
        if self.publicar_joint_states:
            self.pub_joint.publish(msg)
        with self.lock:
            self.q_actual = list(q)

    def publicar_estado_cola(self):
        msg = QueueState()
        msg.stamp = self.get_clock().now().to_msg()
        with self.lock:
            ej = self.ejecutando
            msg.executing_client = ej.client_id if ej else ''
            msg.executing_goal_id = ej.goal_id if ej else ''
            msg.executing_elapsed_s = ((time.time() - ej.t_inicio_ejec)
                                       if ej and ej.t_inicio_ejec else 0.0)
            msg.queue_length = len(self.pendientes)
            msg.queued_goal_ids = [p.goal_id for p in self.pendientes]
            msg.queued_clients = [p.client_id for p in self.pendientes]
            msg.queued_priorities = [min(255, max(0, p.priority)) for p in self.pendientes]
            msg.queued_wait_s = [p.espera_s for p in self.pendientes]
            msg.total_accepted = self.n_aceptados
            msg.total_rejected = self.n_rechazados
            msg.total_completed = self.n_completados
            cola = list(self.pendientes)
        self.pub_cola.publish(msg)

        for posicion, p in enumerate(cola, start=1):
            try:
                fb = PickPlace.Feedback() if p.tipo_pick else MoveArm.Feedback()
                fb.state = 'QUEUED'
                fb.queue_position = posicion
                fb.elapsed_s = p.espera_s
                p.goal_handle.publish_feedback(fb)
            except Exception:
                pass

    def destroy_node(self):
        self._parar.set()
        if hasattr(self, 'worker') and self.worker is not threading.current_thread():
            self.worker.join(timeout=5.0)
        return super().destroy_node()


# ==========================================================================
# Entrada
# ==========================================================================

def _captura_cli(argv):
    """Proceso hijo de la cámara: python3 -m arm_broker.broker --captura ENTRADA SALIDA."""
    solicitud = json.loads(Path(argv[0]).read_text(encoding='utf-8'))
    resultado = capturar_sin_mover(solicitud)
    Path(argv[1]).write_text(json.dumps(resultado), encoding='utf-8')
    return 0


def main(args=None):
    rclpy.init(args=args)
    nodo = ArmBroker()
    # 8 hilos: holgura para que un movimiento de 3 s no deje sin hilo a la admisión
    executor = MultiThreadedExecutor(num_threads=8)
    executor.add_node(nodo)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    if len(sys.argv) > 3 and sys.argv[1] == '--captura':
        sys.exit(_captura_cli(sys.argv[2:4]))
    main()
