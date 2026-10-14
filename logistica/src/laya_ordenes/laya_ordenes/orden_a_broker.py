"""Puente para LA VERSION adjunta del broker (campo joint_positions): servicio /interpretar_orden -> action /move_arm.

NO hace visión, IK, planificación MoveIt2 ni gripper. Solo envía una pose
articular PRECALIBRADA para acercamiento cuando el operador habilita ejecución.
No publica jamás en /joint_states.
"""
import json
import math
import os

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from arm_broker_interfaces.action import MoveArm
from arm_broker import fk
from laya_ordenes_interfaces.srv import InterpretarOrden


class OrdenABroker(Node):
    def __init__(self):
        super().__init__('orden_a_broker')
        self.declare_parameter('frase', '')
        self.declare_parameter('mapa_poses', '')
        self.declare_parameter('habilitar_movimiento', False)  # gate de envío; NO activa salida física del broker
        self.declare_parameter('client_id', 'laya_jetcobot')
        self.interprete = self.create_client(InterpretarOrden, '/interpretar_orden')
        self.broker = ActionClient(self, MoveArm, 'move_arm')

    def correr(self):
        frase = str(self.get_parameter('frase').value).strip()
        habilitar = bool(self.get_parameter('habilitar_movimiento').value)
        mapa = str(self.get_parameter('mapa_poses').value).strip()
        if not frase:
            self.get_logger().error('Proporciona -p frase:=...')
            return False
        if not self.interprete.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('/interpretar_orden no está disponible')
            return False
        req = InterpretarOrden.Request()
        req.frase = frase
        futura = self.interprete.call_async(req)
        rclpy.spin_until_future_complete(self, futura, timeout_sec=10.0)
        if not futura.done() or futura.result() is None:
            self.get_logger().error('No llegó la decisión del intérprete')
            return False
        d = futura.result()
        self.get_logger().info(
            f'DECISIÓN: accion={d.accion}, objeto={d.objeto}, color={d.color}, '
            f'prioridad={d.prioridad}, permitido={d.permitido}, degradada={d.degradada}; {d.motivo}')
        if not d.permitido:
            self.get_logger().warn('RECHAZADA antes de entrar a la cola')
            return False
        if d.accion != 'recoger':
            self.get_logger().warn('Este puente de aproximación SOLO admite recoger. '
                                   'Para colocar, falta la lógica de destino/agarrar/soltar.')
            return False
        if not habilitar:
            self.get_logger().info('MODO SEGURO: no se envió ningún goal al broker. '
                                   'Para una prueba supervisada usa -p habilitar_movimiento:=true')
            return True
        if not mapa or not os.path.isfile(mapa):
            self.get_logger().error('mapa_poses inexistente: falta calibración del objeto')
            return False
        with open(mapa, encoding='utf-8') as f:
            poses = json.load(f)
        clave = f'{d.objeto}:{d.color}'
        q = poses.get(clave)
        if not isinstance(q, list) or len(q) != 6 or not all(
            isinstance(x, (float, int)) and math.isfinite(x) for x in q
        ):
            self.get_logger().error(f'Falta pose de aproximación válida (6 radianes) para {clave}')
            return False
        q = list(map(float, q))
        ok, razon = fk.dentro_de_limites(q)
        if ok:
            ok, razon = fk.dentro_del_workspace(q)
        if not ok:
            self.get_logger().error('Pose rechazada por la FK: ' + razon)
            return False
        if not self.broker.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('No aparece /move_arm; arranca SOLO el broker de ~/logistica; verifica version de la interfaz')
            return False
        goal = MoveArm.Goal()
        goal.joint_positions = q
        goal.client_id = str(self.get_parameter('client_id').value)
        goal.priority = int(d.prioridad)
        enviado = self.broker.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, enviado, timeout_sec=10.0)
        if not enviado.done() or enviado.result() is None:
            self.get_logger().error('No se recibió aceptación del broker')
            return False
        handle = enviado.result()
        if not handle.accepted:
            self.get_logger().warn('El broker rechazó el goal. Mira registro_rechazos.csv')
            return False
        resultado_futuro = handle.get_result_async()
        rclpy.spin_until_future_complete(self, resultado_futuro, timeout_sec=120.0)
        if not resultado_futuro.done() or resultado_futuro.result() is None:
            self.get_logger().error('No llegó el resultado del broker; verifica el estado físico antes de reintentar')
            return False
        res = resultado_futuro.result().result
        self.get_logger().info(f'BROKER (si publica_joint_states=false es SIMULADO): éxito={res.success}; {res.message}; '
                               f'espera={res.wait_time_s:.2f}s, ejecución={res.exec_time_s:.2f}s')
        return res.success


def main(args=None):
    rclpy.init(args=args)
    nodo = OrdenABroker()
    try:
        nodo.correr()
    finally:
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
