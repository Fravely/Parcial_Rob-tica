"""Cliente común de la cadena: frase -> /interpretar_orden -> broker (PickPlace).

Lo usan interfaz_ordenes.py (prompt escrito desde el navegador) y
transcriptor_voz.py (Pregunta 3). Reglas que respeta:

* Nunca habla con la computadora Windows: solo llama al servicio ROS 2
  /interpretar_orden (el nodo interprete_ordenes es el único que consulta LAYA).
* Nunca publica comandos al brazo: solo envía goals a la acción del broker.
  El worker del broker sigue siendo el único publicador (regla del RB-2).
* Una orden con permitido=False se rechaza ANTES de encolarse, con su motivo.

Todos los tiempos se guardan con time.time() (época, para cruzar con el bag)
y las duraciones con time.perf_counter().
"""
import threading
import time
import uuid

from rclpy.action import ActionClient

from laya_ordenes_interfaces.srv import InterpretarOrden

try:  # Acción del broker con agarre (broker fusionado: /logistica/pick_place)
    from arm_broker_interfaces.action import PickPlace
except ImportError:  # versión antigua: solo MoveArm (no sirve para objeto/color)
    PickPlace = None

try:
    from arm_broker_interfaces.msg import QueueState
except ImportError:
    QueueState = None


CAMPOS_DECISION = ('accion', 'objeto', 'color', 'prioridad', 'permitido', 'degradada',
                   'fuente', 'motivo', 'latencia_http_ms', 'inferencia_ms', 'resto_http_ms')

ESTADOS_ESPERA = ('QUEUED', 'EN_COLA', 'ENCOLADO', 'ESPERANDO', 'PENDING', 'PENDIENTE',
                  'ACCEPTED', 'ACEPTADO', 'WAITING')
PREFIJOS_MOVIMIENTO = ('EXECUTING', 'EJECUT', 'POSTURA', 'IR_', 'MOV', 'ABRIR_PINZA')


def _ahora():
    return time.time()


class Seguimiento:
    """Estado vivo de un pedido enviado al broker (lo actualizan los callbacks)."""

    def __init__(self, pedido_id, cliente, frase, decision):
        self.id = pedido_id
        self.cliente = cliente
        self.frase = frase
        self.decision = decision
        self.estado = 'creado'
        self.mensaje = ''
        self.t_creado = _ahora()     # época: llegó la orden
        self.t_envio = None          # época: goal enviado al broker
        self.t_aceptado = None       # época: broker aceptó (entró a la cola)
        self.t_salida_cola = None    # época: primer feedback que ya no es espera
        self.t_inicio_mov = None     # época: primer feedback de movimiento
        self.t_fin = None            # época: llegó el resultado
        self.posicion_cola = None
        self.feedback = []           # [(época, estado, posición)]
        self.exito = None
        self.wait_time_s = None
        self.exec_time_s = None
        # Campos extra del PickPlace de broker_parte3 (si existen en el resultado)
        self.physical_verified = None
        self.position_error_mm = None
        self.etapas = []             # [(etapa, segundos)] informadas por el broker
        self.terminado = threading.Event()

    def como_dict(self):
        return {
            'id': self.id, 'cliente': self.cliente, 'frase': self.frase,
            'decision': self.decision, 'estado': self.estado, 'mensaje': self.mensaje,
            't_creado': self.t_creado, 't_envio': self.t_envio, 't_aceptado': self.t_aceptado,
            't_salida_cola': self.t_salida_cola, 't_inicio_mov': self.t_inicio_mov,
            't_fin': self.t_fin, 'posicion_cola': self.posicion_cola,
            'feedback': list(self.feedback[-30:]), 'exito': self.exito,
            'wait_time_s': self.wait_time_s, 'exec_time_s': self.exec_time_s,
            'physical_verified': self.physical_verified,
            'position_error_mm': self.position_error_mm, 'etapas': list(self.etapas),
        }


class ClienteCadena:
    """Envoltorio thread-safe para usar desde hilos que no son del executor.

    El nodo debe estar girando en un MultiThreadedExecutor en otro hilo.
    """

    def __init__(self, nodo, nombre_accion='/logistica/pick_place', estados_espera=ESTADOS_ESPERA,
                 prefijos_movimiento=PREFIJOS_MOVIMIENTO, al_actualizar=None, topico_cola=''):
        self.nodo = nodo
        self.log = nodo.get_logger()
        self.estados_espera = {s.upper() for s in estados_espera}
        self.prefijos_movimiento = tuple(p.upper() for p in prefijos_movimiento)
        self.al_actualizar = al_actualizar or (lambda seg: None)
        self._lock_envio = threading.Lock()
        self.cli_interprete = nodo.create_client(InterpretarOrden, '/interpretar_orden')
        self.cli_broker = None
        if PickPlace is not None:
            self.cli_broker = ActionClient(nodo, PickPlace, nombre_accion)
        else:
            self.log.warn('arm_broker_interfaces/action/PickPlace no existe en este '
                          'workspace: solo se interpretará, no se encolará.')
        self.estado_cola = None
        if not topico_cola:
            # /logistica/pick_place -> /logistica/arm/queue_state ; /pick_place -> /arm/queue_state
            base = nombre_accion.rsplit('/', 1)[0]
            topico_cola = base + '/arm/queue_state'
        self.topico_cola = topico_cola
        if QueueState is not None:
            nodo.create_subscription(QueueState, topico_cola, self._cola, 10)

    # ------------------------------------------------------------ cola
    def _cola(self, msg):
        self.estado_cola = {
            'ejecutando': msg.executing_client,
            'ejecutando_s': round(float(msg.executing_elapsed_s), 2),
            'longitud': int(msg.queue_length),
            'clientes': list(msg.queued_clients),
            'prioridades': [int(p) for p in msg.queued_priorities],
            'espera_s': [round(float(w), 2) for w in msg.queued_wait_s],
            'aceptados': int(msg.total_accepted),
            'rechazados': int(msg.total_rejected),
            'completados': int(msg.total_completed),
            't': _ahora(),
        }

    # ------------------------------------------------------- utilidades
    @staticmethod
    def _esperar(futuro, timeout_s):
        evento = threading.Event()
        futuro.add_done_callback(lambda _f: evento.set())
        if futuro.done():
            evento.set()
        return evento.wait(timeout_s)

    def interprete_listo(self, timeout_s=0.5):
        return self.cli_interprete.wait_for_service(timeout_sec=timeout_s)

    def broker_listo(self, timeout_s=0.5):
        return self.cli_broker is not None and self.cli_broker.wait_for_server(timeout_sec=timeout_s)

    # ------------------------------------------------- interpretación
    def interpretar(self, frase, timeout_s=5.0):
        """Devuelve (decision_dict, ms_cliente). Lanza TimeoutError si no responde."""
        if not self.interprete_listo(min(timeout_s, 2.0)):
            raise RuntimeError('/interpretar_orden no está disponible en este ROS_DOMAIN_ID')
        req = InterpretarOrden.Request()
        req.frase = frase
        inicio = time.perf_counter()
        with self._lock_envio:
            futuro = self.cli_interprete.call_async(req)
        if not self._esperar(futuro, timeout_s):
            try:
                self.cli_interprete.remove_pending_request(futuro)
            except Exception:
                pass
            raise TimeoutError(f'/interpretar_orden no respondió en {timeout_s:.1f} s')
        ms = (time.perf_counter() - inicio) * 1000.0
        r = futuro.result()
        decision = {c: getattr(r, c) for c in CAMPOS_DECISION if hasattr(r, c)}
        decision['prioridad'] = int(decision.get('prioridad', 0))
        decision['permitido'] = bool(decision.get('permitido', False))
        return decision, ms

    # ------------------------------------------------------ broker
    def enviar_al_broker(self, decision, cliente, frase, zona='deposito'):
        """Encola en el broker SOLO si la decisión lo permite. Devuelve Seguimiento."""
        seg = Seguimiento(uuid.uuid4().hex[:8], cliente, frase, decision)
        if not decision.get('permitido'):
            seg.estado = 'rechazada_antes_de_encolar'
            seg.mensaje = decision.get('motivo', 'no permitida')
            seg.terminado.set()
            self.al_actualizar(seg)
            return seg
        if not self.broker_listo(2.0):
            seg.estado = 'sin_broker'
            seg.mensaje = 'La acción del broker no está disponible (¿broker apagado o versión MoveArm?)'
            seg.terminado.set()
            self.al_actualizar(seg)
            return seg

        goal = PickPlace.Goal()
        campos = goal.get_fields_and_field_types()
        valores = {
            'client_id': cliente,
            'priority': max(0, min(255, int(decision.get('prioridad', 0)))),
            'accion': decision.get('accion', ''),
            'objeto': decision.get('objeto', ''),
            'color': decision.get('color', ''),
            'zona': zona,
            'permitido': bool(decision.get('permitido')),
            'degradada': bool(decision.get('degradada')),
            'fuente': decision.get('fuente', ''),
        }
        for campo, valor in valores.items():
            if campo in campos:
                setattr(goal, campo, valor)

        def feedback(msg):
            f = msg.feedback
            estado = str(getattr(f, 'state', ''))
            pos = int(getattr(f, 'queue_position', -1))
            t = _ahora()
            # El broker repite QUEUED a 5 Hz: guardar solo los cambios de estado/posición.
            if not seg.feedback or seg.feedback[-1][1:] != (estado, pos):
                seg.feedback.append((round(t, 3), estado, pos))
            seg.posicion_cola = pos
            ESTADO = estado.upper()
            espera = ESTADO in self.estados_espera or pos > 0
            if not espera and seg.t_salida_cola is None:
                seg.t_salida_cola = t
            if seg.t_inicio_mov is None and ESTADO.startswith(self.prefijos_movimiento):
                seg.t_inicio_mov = t
                if seg.t_salida_cola is None:
                    seg.t_salida_cola = t
            seg.estado = 'en_cola' if espera else 'ejecutando'
            seg.mensaje = estado
            self.al_actualizar(seg)

        seg.t_envio = _ahora()
        seg.estado = 'enviado'
        with self._lock_envio:
            futuro = self.cli_broker.send_goal_async(goal, feedback_callback=feedback)

        def aceptado(fut):
            try:
                handle = fut.result()
            except Exception as exc:
                seg.estado, seg.mensaje = 'error', str(exc)
                seg.terminado.set()
                self.al_actualizar(seg)
                return
            if not handle.accepted:
                seg.estado = 'rechazada_por_broker'
                seg.mensaje = 'El broker rechazó el goal (ver registro_rechazos.csv)'
                seg.t_fin = _ahora()
                seg.terminado.set()
                self.al_actualizar(seg)
                return
            seg.t_aceptado = _ahora()
            seg.estado = 'en_cola'
            self.al_actualizar(seg)
            handle.get_result_async().add_done_callback(resultado)

        def resultado(fut):
            seg.t_fin = _ahora()
            try:
                r = fut.result().result
                seg.exito = bool(getattr(r, 'success', False))
                seg.mensaje = str(getattr(r, 'message', ''))
                seg.wait_time_s = float(getattr(r, 'wait_time_s', -1.0))
                seg.exec_time_s = float(getattr(r, 'exec_time_s', -1.0))
                if hasattr(r, 'physical_verified'):
                    seg.physical_verified = bool(r.physical_verified)
                if hasattr(r, 'position_error_mm'):
                    seg.position_error_mm = float(r.position_error_mm)
                seg.etapas = [(str(e), round(float(t), 3)) for e, t in
                              zip(getattr(r, 'stages', []), getattr(r, 'stage_time_s', []))]
                seg.estado = 'completada' if seg.exito else 'fallida'
            except Exception as exc:
                seg.estado, seg.mensaje = 'error', str(exc)
            seg.terminado.set()
            self.al_actualizar(seg)

        futuro.add_done_callback(aceptado)
        self.al_actualizar(seg)
        return seg
