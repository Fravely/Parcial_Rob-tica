"""Texto -> interprete -> PickPlace. Zona por parametro; sin publicacion al brazo."""
import sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from arm_broker_interfaces.action import PickPlace
from laya_ordenes_interfaces.srv import InterpretarOrden

class OrdenARecogida(Node):
    def __init__(self):
        super().__init__('orden_a_recogida')
        self.declare_parameter('frase', '')
        self.declare_parameter('client_id', 'operador')
        self.declare_parameter('zona', 'deposito')
        self.declare_parameter('enviar_pedido', False)
        self.declare_parameter('permitir_respaldo', False)
        self.declare_parameter('timeout_resultado_s', 900.0)
        self.interprete = self.create_client(InterpretarOrden, '/interpretar_orden')
        self.broker = ActionClient(self, PickPlace, 'pick_place')
    def esperar(self, futuro, segundos):
        rclpy.spin_until_future_complete(self, futuro, timeout_sec=segundos)
        if not futuro.done():
            raise TimeoutError('no llego respuesta; revisar estado antes de reintentar')
        valor = futuro.result()
        if valor is None:
            raise RuntimeError('respuesta vacia')
        return valor
    def correr(self):
        limite = float(self.get_parameter('timeout_resultado_s').value)
        if not 1 <= limite <= 3600:
            raise ValueError('timeout_resultado_s debe estar entre 1 y 3600')
        frase = str(self.get_parameter('frase').value).strip()
        if not frase:
            raise ValueError('falta parametro frase')
        if not self.interprete.wait_for_service(timeout_sec=5.0):
            raise RuntimeError('no aparece /interpretar_orden')
        req = InterpretarOrden.Request()
        req.frase = frase
        d = self.esperar(self.interprete.call_async(req), 10.0)
        self.get_logger().info(f'DECISION: {d.accion} {d.objeto} {d.color}; prioridad={d.prioridad}; '
                               f'permitido={d.permitido}; fuente={d.fuente}; {d.motivo}')
        if not d.permitido or d.accion != 'recoger':
            self.get_logger().warn('RECHAZADO antes de encolar: ' + d.motivo)
            return False
        if d.degradada and not self.get_parameter('permitir_respaldo').value:
            self.get_logger().warn('Respaldo no habilitado para esta prueba')
            return False
        if not self.get_parameter('enviar_pedido').value:
            self.get_logger().info('Solo interpretacion; no se envio pedido')
            return True
        if not self.broker.wait_for_server(timeout_sec=5.0):
            raise RuntimeError('no aparece /pick_place')
        goal = PickPlace.Goal()
        goal.client_id = str(self.get_parameter('client_id').value)
        goal.priority = int(d.prioridad)
        for campo in ('accion', 'objeto', 'color', 'permitido', 'degradada', 'fuente'):
            setattr(goal, campo, getattr(d, campo))
        goal.zona = str(self.get_parameter('zona').value)
        handle = self.esperar(self.broker.send_goal_async(goal, feedback_callback=self.feedback), 10.0)
        if not handle.accepted:
            self.get_logger().warn('Broker rechazo el pedido; consultar su log')
            return False
        try:
            res = self.esperar(handle.get_result_async(), limite).result
        except TimeoutError:
            handle.cancel_goal_async()
            raise TimeoutError('se solicito cancelar por timeout; verificar estado del broker antes de reenviar')
        self.get_logger().info(f'RESULTADO: success={res.success}; simulado={res.simulated}; '
                               f'solo_planificacion={res.planning_only}; verificado_fisico={res.physical_verified}; {res.message}')
        for etapa, segundos in zip(res.stages, res.stage_time_s):
            self.get_logger().info(f'{etapa}: {segundos:.3f}s')
        return res.success
    def feedback(self, msg):
        f = msg.feedback
        self.get_logger().info(f'{f.state}: cola={f.queue_position}, t={f.elapsed_s:.2f}s')

def main(args=None):
    rclpy.init(args=args)
    nodo = OrdenARecogida()
    codigo = 1
    try:
        codigo = 0 if nodo.correr() else 1
    except (Exception, KeyboardInterrupt) as exc:
        nodo.get_logger().error(str(exc))
    finally:
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    sys.exit(codigo)
