"""Cliente interactivo de cada integrante (Pregunta 2 con LAYA).

    texto -> servicio /interpretar_orden (LAYA, o respaldo si LAYA no responde)
          -> si permitido=True  -> accion PickPlace del broker (cola RB-2)
          -> si permitido=False -> RECHAZADA ANTES DE ENCOLAR, con su causa

Reglas que respeta:
  * La prioridad del goal es la que devolvio el modelo (no se escribe a mano).
  * Nunca habla con la PC Windows: solo con el servicio /interpretar_orden.
  * Nunca abre el puerto serie ni publica al brazo: el worker del broker es el unico.

Uso (lo lanza scripts/cliente.sh):
    ros2 run laya_ordenes cliente_laya --nombre integrante1
    ros2 run laya_ordenes cliente_laya --nombre integrante1 --orden "recoge el cubo rojo"
"""
import argparse
import csv
import datetime
import os
import re
import sys
import threading
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.signals import SignalHandlerOptions

from arm_broker_interfaces.action import PickPlace
from laya_ordenes_interfaces.srv import InterpretarOrden

COLUMNAS = ['fecha', 'cliente', 'frase', 'accion', 'objeto', 'color', 'prioridad',
            'permitido', 'degradada', 'fuente', 'motivo', 'decision_ms', 'estado',
            'wait_time_s', 'exec_time_s', 'mensaje_broker']


class ClienteLaya(Node):
    def __init__(self, nombre, accion, timeout_decision_s, registro_dir, zona):
        identificador = re.sub(r'[^a-zA-Z0-9_]', '_', nombre)
        super().__init__('cliente_laya_' + identificador)
        self.nombre = nombre
        self.accion = accion
        self.zona = zona
        self.timeout_decision = timeout_decision_s
        self.interprete = self.create_client(InterpretarOrden, '/interpretar_orden')
        self.cliente = ActionClient(self, PickPlace, accion)
        self.activo = None
        self.ultimo_feedback = None
        self.csv = ''
        if registro_dir:
            os.makedirs(registro_dir, exist_ok=True)
            self.csv = os.path.join(registro_dir, identificador + '.csv')
        self._lock = threading.Lock()

    # ------------------------------------------------------------ registro
    def _registrar(self, fila):
        if not self.csv:
            return
        try:
            with self._lock:
                nuevo = not os.path.exists(self.csv) or os.path.getsize(self.csv) == 0
                with open(self.csv, 'a', newline='', encoding='utf-8') as f:
                    w = csv.DictWriter(f, fieldnames=COLUMNAS)
                    if nuevo:
                        w.writeheader()
                    w.writerow({k: fila.get(k, '') for k in COLUMNAS})
        except OSError as exc:
            print(f'(no se pudo escribir {self.csv}: {exc})', flush=True)

    # ------------------------------------------------------------ decision
    def interpretar(self, frase):
        if not self.interprete.wait_for_service(timeout_sec=5.0):
            raise RuntimeError('no existe /interpretar_orden: arranca bash scripts/interprete.sh')
        req = InterpretarOrden.Request()
        req.frase = frase
        inicio = time.perf_counter()
        futuro = self.interprete.call_async(req)
        rclpy.spin_until_future_complete(self, futuro, timeout_sec=self.timeout_decision)
        if not futuro.done():
            try:
                self.interprete.remove_pending_request(futuro)
            except Exception:
                pass
            raise TimeoutError(f'/interpretar_orden no respondio en {self.timeout_decision:.1f} s')
        respuesta = futuro.result()
        if respuesta is None:
            raise RuntimeError('respuesta vacia de /interpretar_orden')
        return respuesta, (time.perf_counter() - inicio) * 1000.0

    def feedback(self, msg):
        f = msg.feedback
        clave = (f.state, f.queue_position)
        if clave != self.ultimo_feedback:
            print(f'[{self.nombre}] {f.state} | posicion en cola: {f.queue_position}', flush=True)
            self.ultimo_feedback = clave

    # ------------------------------------------------------------ envio
    def enviar(self, frase):
        fila = dict(fecha=datetime.datetime.now().isoformat(timespec='milliseconds'),
                    cliente=self.nombre, frase=frase)
        try:
            d, ms = self.interpretar(frase)
        except Exception as exc:
            print(f'[{self.nombre}] SIN DECISION: {exc}', flush=True)
            fila.update(estado='sin_decision', mensaje_broker=str(exc))
            self._registrar(fila)
            return 1
        fila.update(accion=d.accion, objeto=d.objeto, color=d.color, prioridad=d.prioridad,
                    permitido=d.permitido, degradada=d.degradada, fuente=d.fuente,
                    motivo=d.motivo, decision_ms=round(ms, 1))
        print(f'[{self.nombre}] DECISION ({d.fuente}{", degradada" if d.degradada else ""}, '
              f'{ms:.0f} ms): {d.accion} {d.objeto} {d.color} | prioridad {d.prioridad} | '
              f'permitido={d.permitido}', flush=True)
        if not d.permitido:
            print(f'[{self.nombre}] RECHAZADA ANTES DE ENCOLAR: {d.motivo}', flush=True)
            fila['estado'] = 'rechazada_antes_de_encolar'
            self._registrar(fila)
            return 2
        if not self.cliente.wait_for_server(timeout_sec=15.0):
            print(f'No responde {self.accion}. Inicia el broker: bash scripts/broker.sh', flush=True)
            fila['estado'] = 'sin_broker'
            self._registrar(fila)
            return 1
        goal = PickPlace.Goal()
        goal.client_id = self.nombre
        goal.priority = max(0, min(255, int(d.prioridad)))   # la decide el modelo
        goal.accion = d.accion
        goal.objeto = d.objeto
        goal.color = d.color
        goal.zona = self.zona
        goal.permitido = bool(d.permitido)
        goal.degradada = bool(d.degradada)
        goal.fuente = d.fuente
        self.ultimo_feedback = None
        envio = self.cliente.send_goal_async(goal, feedback_callback=self.feedback)
        rclpy.spin_until_future_complete(self, envio)
        self.activo = envio.result()
        if self.activo is None or not self.activo.accepted:
            self.activo = None
            print(f'[{self.nombre}] RECHAZADA POR EL BROKER (motivo en su terminal y en '
                  'evidencias/pregunta2/rechazos.csv)', flush=True)
            fila['estado'] = 'rechazada_por_broker'
            self._registrar(fila)
            return 2
        try:
            futuro = self.activo.get_result_async()
            rclpy.spin_until_future_complete(self, futuro)
            respuesta = futuro.result()
            if respuesta is None:
                raise RuntimeError('El broker no devolvio resultado.')
            r = respuesta.result
            print(f"[{self.nombre}] {'COMPLETADO' if r.success else 'FALLO'}: {r.message}\n"
                  f'Espera en cola: {r.wait_time_s:.2f}s | ejecucion: {r.exec_time_s:.2f}s',
                  flush=True)
            fila.update(estado='completada' if r.success else 'fallida',
                        wait_time_s=round(r.wait_time_s, 3), exec_time_s=round(r.exec_time_s, 3),
                        mensaje_broker=r.message)
            self._registrar(fila)
            return 0 if r.success else 1
        finally:
            # En una interrupcion se conserva el handle para solicitar cancelacion.
            if sys.exc_info()[0] is None:
                self.activo = None

    def cancelar(self):
        if self.activo is not None and self.activo.accepted and rclpy.ok():
            futuro = self.activo.cancel_goal_async()
            rclpy.spin_until_future_complete(self, futuro, timeout_sec=3.0)
            print('Cancelacion solicitada al broker. La pinza no se abre automaticamente.',
                  flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--nombre', required=True, help='Nombre distinto para cada integrante.')
    parser.add_argument('--orden', help='Una sola orden; si se omite abre el modo interactivo.')
    parser.add_argument('--accion', default=os.environ.get('ACCION_BROKER', '/logistica/pick_place'),
                        help='Accion PickPlace del broker (por defecto /logistica/pick_place).')
    parser.add_argument('--zona', default='deposito')
    parser.add_argument('--timeout-decision', type=float, default=10.0,
                        help='Segundos maximos esperando /interpretar_orden.')
    parser.add_argument('--registro', default=os.path.join(
        os.environ.get('PROYECTO', os.path.expanduser('~/logistica')),
        'evidencias', 'pregunta2', 'clientes'),
        help='Carpeta del CSV de este cliente ("" para no registrar).')
    args = parser.parse_args()
    # Ctrl+C lo gestiona el cliente para poder pedir cancelacion antes de cerrar ROS.
    rclpy.init(args=[], signal_handler_options=SignalHandlerOptions.NO)
    nodo = ClienteLaya(args.nombre, args.accion, args.timeout_decision, args.registro, args.zona)
    codigo = 0
    try:
        if args.orden:
            codigo = nodo.enviar(args.orden)
        else:
            print('Cliente LAYA listo. Escribe una orden por turno; "salir" termina el cliente.',
                  flush=True)
            while rclpy.ok():
                frase = input(f'{args.nombre}> ').strip()
                if frase.casefold() in ('salir', 'exit'):
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


if __name__ == '__main__':
    sys.exit(main())
