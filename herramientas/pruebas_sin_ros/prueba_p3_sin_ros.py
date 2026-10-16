"""Prueba sin ROS de la cadena de la Pregunta 3: transcriptor -> cadena -> broker (doble).

Cubre: sin internet -> MODO TEXTO; orden no permitida -> rechazo antes de encolar;
orden valida -> goal con prioridad del modelo, tiempos de cola y MOVER_AGARRE;
CSV voz_cadena.csv y desglose_tiempos.py sobre ese CSV.
"""
import builtins, io, json, os, sys, tempfile, threading, time, types, urllib.error, subprocess, csv

# Uso: python3 herramientas/pruebas_sin_ros/prueba_p3_sin_ros.py   (no necesita ROS ni robot)
RAIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(RAIZ, 'src', 'laya_ordenes'))

# ------------------------------------------------------------- dobles de ROS
class Msg:
    def __init__(self, **kw): self.__dict__.update(kw)

def modulo(nombre, **attrs):
    m = types.ModuleType(nombre); m.__dict__.update(attrs); sys.modules[nombre] = m; return m

class Param:
    def __init__(self, v): self.value = v

class Node:
    def __init__(self, nombre, **kw):
        self._p = {}; self.nombre = nombre; self.publicados = []
    def declare_parameter(self, n, v): self._p.setdefault(n, v)
    def get_parameter(self, n): return Param(self._p[n])
    def get_logger(self):
        nodo = self
        class L:
            def info(s, m): print('[INFO]', m)
            def warn(s, m): print('[WARN]', m)
            def error(s, m): print('[ERROR]', m)
        return L()
    def create_publisher(self, t, topic, q):
        nodo = self
        class P:
            def publish(s, m): nodo.publicados.append((topic, m.data))
        return P()
    def create_subscription(self, *a, **k): self.sub = a
    def create_client(self, t, nombre): return ServicioFalso()
    def destroy_node(self): pass

class Futuro:
    def __init__(self): self._r = None; self._cbs = []; self._done = False
    def set_result(self, r):
        self._r = r; self._done = True
        for cb in self._cbs: cb(self)
    def result(self): return self._r
    def done(self): return self._done
    def add_done_callback(self, cb):
        self._cbs.append(cb)
        if self._done: cb(self)

DECISIONES = {}
class ServicioFalso:
    def wait_for_service(self, timeout_sec=None): return True
    def call_async(self, req):
        f = Futuro(); f.set_result(Msg(**DECISIONES[req.frase])); return f
    def remove_pending_request(self, f): pass

ENVIADOS = []
class ActionClientFalso:
    def __init__(self, nodo, tipo, nombre): self.nombre = nombre
    def wait_for_server(self, timeout_sec=None): return True
    def send_goal_async(self, goal, feedback_callback=None):
        ENVIADOS.append(goal)
        f = Futuro()
        def correr():
            time.sleep(0.05)
            res_f = Futuro()
            handle = Msg(accepted=True, get_result_async=lambda: res_f)
            f.set_result(handle)
            for estado, pos, dt in [('QUEUED', 1, 0.3), ('PLAN_ESCANEO', 0, 0.1),
                                    ('ESCANEO:IK_MOVEIT2_SOLO_PLAN', 0, 0.05),
                                    ('ESCANEO:TRAYECTORIA_MOVEIT2_SOLO_PLAN', 0, 0.1),
                                    ('MOVER_ESCANEO', 0, 0.2), ('DETECTAR_COLOR', 0, 0.4),
                                    ('LOCALIZADO_ROJO_EN_SUPERIOR_IZQUIERDA', 0, 0.01),
                                    ('ABRIR_PINZA', 0, 0.3), ('PLAN_AGARRE', 0, 0.05),
                                    ('AGARRE:IK_MOVEIT2_SOLO_PLAN', 0, 0.15),
                                    ('AGARRE:TRAYECTORIA_MOVEIT2_SOLO_PLAN', 0, 0.25),
                                    ('MOVER_AGARRE', 0, 0.2), ('CERRAR_PINZA', 0, 0.05)]:
                feedback_callback(Msg(feedback=Msg(state=estado, queue_position=pos, elapsed_s=0)))
                time.sleep(dt)
            res_f.set_result(Msg(result=Msg(success=True, message='CICLO COMPLETADO', wait_time_s=0.3,
                                            exec_time_s=2.0, physical_verified=False,
                                            position_error_mm=1.5, stages=['MOVER_AGARRE'],
                                            stage_time_s=[0.5])))
        threading.Thread(target=correr, daemon=True).start()
        return f

class Goal:
    def get_fields_and_field_types(self):
        return {k: 'x' for k in ('client_id', 'priority', 'accion', 'objeto', 'color', 'zona',
                                 'permitido', 'degradada', 'fuente')}

modulo('rclpy', ok=lambda: True, init=lambda **k: None, shutdown=lambda: None)
modulo('rclpy.node', Node=Node)
modulo('rclpy.action', ActionClient=ActionClientFalso)
modulo('rclpy.executors', MultiThreadedExecutor=object)
modulo('std_msgs'); modulo('std_msgs.msg', String=lambda: Msg(data=''))
modulo('laya_ordenes_interfaces'); modulo('laya_ordenes_interfaces.srv',
       InterpretarOrden=Msg(Request=lambda: Msg(frase='')))
modulo('arm_broker_interfaces'); modulo('arm_broker_interfaces.action', PickPlace=Msg(Goal=Goal))
modulo('arm_broker_interfaces.msg', QueueState=object)

from laya_ordenes import transcriptor_voz as tv

tmp = tempfile.mkdtemp()
class TV(tv.TranscriptorVoz):
    def __init__(self):
        Node.__init__(self, 'transcriptor_voz')
        self._p.update(dir_evidencias=tmp, enviar_al_broker=True, timeout_transcripcion_s=1.0)
        tv.TranscriptorVoz.__init__(self)
# Node.__init__ se llamaria dos veces; neutralizamos el super() del transcriptor
_orig_init = Node.__init__
def _init(self, nombre, **kw):
    if not hasattr(self, '_p'): _orig_init(self, nombre, **kw)
Node.__init__ = _init

os.environ['GEMINI_API_KEY'] = 'clave-falsa-solo-para-la-prueba'
nodo = TV()
assert nodo.cadena.topico_cola == '/logistica/arm/queue_state', nodo.cadena.topico_cola
assert nodo.inicio_mov == 'MOVER_AGARRE'

# --- 1) Sin internet: gemini_rest lanza URLError -> modo texto -> teclado
def sin_red(*a, **k): raise urllib.error.URLError('Temporary failure in name resolution')
tv.gemini_rest = sin_red
DECISIONES['recoge el cubo rojo urgente'] = dict(accion='recoger', objeto='cubo', color='rojo',
    prioridad=68, permitido=True, degradada=False, fuente='LAYA', motivo='ok',
    latencia_http_ms=150.0, inferencia_ms=130.0, resto_http_ms=20.0)
wav = os.path.join(tmp, 'orden_01_x.wav')
import wave
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000); w.writeframes(b'\x00\x00' * 16000)
entradas = iter(['recoge el cubo rojo urgente'])
builtins.input = lambda *a: next(entradas)
t = time.perf_counter()
nodo.procesar(wav, t, time.time(), t + 0.01)
nodo.esperar_pendientes()
time.sleep(0.2)
assert ENVIADOS and ENVIADOS[-1].priority == 68 and ENVIADOS[-1].fuente == 'LAYA'
assert any(tp == '/voz/estado' and d.startswith('MODO_TEXTO') for tp, d in nodo.publicados)

# --- 2) Voz OK + orden no permitida -> rechazo antes de encolar
tv.gemini_rest = lambda *a, **k: 'recoge la botella verde'
DECISIONES['recoge la botella verde'] = dict(accion='recoger', objeto='ninguno', color='verde',
    prioridad=80, permitido=False, degradada=False, fuente='LAYA',
    motivo='objeto desconocido o no disponible en el inventario', latencia_http_ms=140.0,
    inferencia_ms=120.0, resto_http_ms=20.0)
n_antes = len(ENVIADOS)
t = time.perf_counter()
nodo.procesar(wav, t, time.time(), t + 0.01)
assert len(ENVIADOS) == n_antes, 'una orden no permitida NO debe llegar al broker'

# --- 3) Voz OK + orden valida -> broker, tiempos hasta MOVER_AGARRE
tv.gemini_rest = lambda *a, **k: 'recoge el cubo rojo urgente'
t = time.perf_counter()
nodo.procesar(wav, t, time.time(), t + 0.01)
nodo.esperar_pendientes(); time.sleep(0.2)

with open(os.path.join(tmp, 'voz_cadena.csv'), encoding='utf-8') as f:
    filas = list(csv.DictReader(f))
for r in filas:
    print(r['n'], r['modo'], r['transcripcion'], r['estado_broker'], r['espera_cola_ms'],
          r['salida_cola_a_movimiento_ms'], r['voz_a_movimiento_ms'])
assert filas[0]['modo'] == 'texto' and 'URLError' in filas[0]['motivo_modo_texto'] or 'ConnectionError' in filas[0]['motivo_modo_texto']
assert filas[1]['estado_broker'] == 'rechazada_antes_de_encolar'
assert filas[2]['modo'] == 'voz' and filas[2]['estado_broker'] == 'completada'
assert float(filas[2]['salida_cola_a_movimiento_ms']) > 1500, 'debe incluir camara, IK y plan'
assert os.path.exists(os.path.splitext(wav)[0] + '.json')

# --- 4) desglose_tiempos.py sobre el CSV generado
r = subprocess.run([sys.executable, os.path.join(RAIZ, 'herramientas', 'desglose_tiempos.py'),
                    '--csv', os.path.join(tmp, 'voz_cadena.csv')], capture_output=True, text=True)
print(r.stdout[-1500:]); print(r.stderr[-800:])
assert r.returncode == 0
print(open(os.path.join(tmp, 'desglose_tiempos.md'), encoding='utf-8').read())
print('PRUEBA P3 SIN ROS: OK')
