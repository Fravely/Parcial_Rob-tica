"""Cliente interactivo SIN LAYA: texto -> reglas locales -> acción PickPlace del broker.

Respaldo para cuando el servidor LAYA no está disponible. El camino normal es
scripts/cliente.sh (texto -> /interpretar_orden -> broker).
"""
import argparse
import os
import re
import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions
from arm_broker_interfaces.action import PickPlace
from arm_broker.orden_local import interpretar


class ClienteSinLaya(Node):
    def __init__(self, nombre, accion):
        identificador = re.sub(r"[^a-zA-Z0-9_]", "_", nombre)
        super().__init__("cliente_sin_laya_" + identificador)
        self.nombre = nombre
        self.accion = accion
        self.cliente = ActionClient(self, PickPlace, accion)
        self.activo = None
        self.ultimo_feedback = None

    def feedback(self, msg):
        f = msg.feedback
        clave = (f.state, f.queue_position)
        if clave != self.ultimo_feedback:
            print(f"[{self.nombre}] {f.state} | posición en cola: {f.queue_position}", flush=True)
            self.ultimo_feedback = clave

    def enviar(self, frase):
        try:
            decision = interpretar(frase)
        except ValueError as exc:
            print(f"RECHAZADO: {exc}", flush=True)
            return 2
        print(f"[{self.nombre}] {decision['color']} -> depósito | prioridad "
              f"{decision['priority']} | fuente LOCAL_SIN_LAYA", flush=True)
        if not self.cliente.wait_for_server(timeout_sec=15.0):
            print(f"No responde {self.accion}. Inicia el broker: bash scripts/broker.sh", flush=True)
            return 1
        goal = PickPlace.Goal()
        goal.client_id = self.nombre
        for campo, valor in decision.items():
            setattr(goal, campo, valor)
        self.ultimo_feedback = None
        envio = self.cliente.send_goal_async(goal, feedback_callback=self.feedback)
        rclpy.spin_until_future_complete(self, envio)
        self.activo = envio.result()
        if self.activo is None or not self.activo.accepted:
            self.activo = None
            print("RECHAZADO por el broker; el motivo aparece en su terminal.", flush=True)
            return 2
        try:
            futuro = self.activo.get_result_async()
            rclpy.spin_until_future_complete(self, futuro)
            respuesta = futuro.result()
            if respuesta is None:
                raise RuntimeError("El broker no devolvió resultado.")
            r = respuesta.result
            print(f"[{self.nombre}] {'COMPLETADO' if r.success else 'FALLO'}: {r.message}\n"
                  f"Espera: {r.wait_time_s:.2f}s | ejecución: {r.exec_time_s:.2f}s",
                  flush=True)
            return 0 if r.success else 1
        finally:
            # En una interrupción se conserva el handle para solicitar cancelación.
            if sys.exc_info()[0] is None:
                self.activo = None

    def cancelar(self):
        if self.activo is not None and self.activo.accepted and rclpy.ok():
            futuro = self.activo.cancel_goal_async()
            rclpy.spin_until_future_complete(self, futuro, timeout_sec=3.0)
            print("Cancelación solicitada al broker. La pinza no se abre automáticamente.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nombre", required=True, help="Nombre distinto para cada integrante.")
    parser.add_argument("--orden", help="Una sola orden; si se omite abre el modo interactivo.")
    parser.add_argument("--accion", default=os.environ.get("ACCION_BROKER", "/logistica/pick_place"),
                        help="Acción PickPlace del broker (por defecto /logistica/pick_place).")
    args = parser.parse_args()
    # Ctrl+C lo gestiona el cliente para poder pedir cancelación antes de cerrar ROS.
    rclpy.init(args=[], signal_handler_options=SignalHandlerOptions.NO)
    nodo = ClienteSinLaya(args.nombre, args.accion)
    codigo = 0
    try:
        if args.orden:
            codigo = nodo.enviar(args.orden)
        else:
            print("Cliente listo. Escribe una orden por turno; 'salir' termina el cliente.",
                  flush=True)
            while rclpy.ok():
                frase = input(f"{args.nombre}> ").strip()
                if frase.casefold() in ("salir", "exit"):
                    break
                if frase:
                    nodo.enviar(frase)
    except (KeyboardInterrupt, EOFError):
        nodo.cancelar()
    finally:
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    return codigo


if __name__ == "__main__":
    sys.exit(main())
