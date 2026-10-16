"""Prueba sin ROS de cliente_laya: rechazo antes de encolar y prioridad del modelo en el goal."""
import os, sys, types, tempfile, csv
# Uso: python3 herramientas/pruebas_sin_ros/prueba_cliente_laya.py   (no necesita ROS ni robot)
RAIZ = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(RAIZ, 'src', 'laya_ordenes'))
class Msg:
    def __init__(self, **kw): self.__dict__.update(kw)
def modulo(n, **a):
    m = types.ModuleType(n); m.__dict__.update(a); sys.modules[n] = m
class F:
    def __init__(self, r): self._r = r
    def done(self): return True
    def result(self): return self._r
DEC = {}
class Srv:
    def wait_for_service(self, timeout_sec=None): return True
    def call_async(self, req): return F(Msg(**DEC[req.frase]))
GOALS = []
class AC:
    def __init__(self, n, t, nombre): self.nombre = nombre
    def wait_for_server(self, timeout_sec=None): return True
    def send_goal_async(self, goal, feedback_callback=None):
        GOALS.append(goal)
        feedback_callback(Msg(feedback=Msg(state='QUEUED', queue_position=2)))
        feedback_callback(Msg(feedback=Msg(state='MOVER_AGARRE', queue_position=0)))
        res = Msg(result=Msg(success=True, message='CICLO COMPLETADO', wait_time_s=3.2, exec_time_s=41.0))
        return F(Msg(accepted=True, get_result_async=lambda: F(res), cancel_goal_async=lambda: F(None)))
class Node:
    def __init__(self, n): self.n = n
    def create_client(self, t, n): return Srv()
    def destroy_node(self): pass
modulo('rclpy', spin_until_future_complete=lambda *a, **k: None, ok=lambda: True)
modulo('rclpy.node', Node=Node); modulo('rclpy.action', ActionClient=AC)
modulo('rclpy.signals', SignalHandlerOptions=Msg(NO=0))
modulo('arm_broker_interfaces'); modulo('arm_broker_interfaces.action', PickPlace=Msg(Goal=lambda: Msg()))
modulo('laya_ordenes_interfaces'); modulo('laya_ordenes_interfaces.srv', InterpretarOrden=Msg(Request=lambda: Msg(frase='')))
from laya_ordenes import cliente_laya as cl
tmp = tempfile.mkdtemp()
c = cl.ClienteLaya('integrante 1', '/logistica/pick_place', 5.0, tmp, 'deposito')
base = dict(objeto='cubo', degradada=False, fuente='LAYA', latencia_http_ms=1.0, inferencia_ms=1.0, resto_http_ms=0.0)
DEC['recoge el cubo azul urgente'] = dict(base, accion='recoger', color='azul', prioridad=68, permitido=True, motivo='ok')
DEC['golpea el cubo rojo'] = dict(base, accion='peligrosa', color='rojo', prioridad=86, permitido=False, motivo='orden negativa o potencialmente peligrosa')
assert c.enviar('golpea el cubo rojo') == 2 and not GOALS
assert c.enviar('recoge el cubo azul urgente') == 0
g = GOALS[-1]
assert (g.priority, g.color, g.fuente, g.client_id, g.zona) == (68, 'azul', 'LAYA', 'integrante 1', 'deposito')
filas = list(csv.DictReader(open(os.path.join(tmp, 'integrante_1.csv'), encoding='utf-8')))
print([ (f['frase'], f['estado'], f['prioridad']) for f in filas])
assert [f['estado'] for f in filas] == ['rechazada_antes_de_encolar', 'completada']
print('PRUEBA cliente_laya: OK')
