"""Servicio ROS 2 /interpretar_orden; nombre del nodo: interprete_ordenes_logistica.

Convierte texto a decision tipada. No publica en /joint_states ni mueve el brazo.
El nombre unico evita colisiones con el nodo antiguo /interprete_ordenes.
"""
import concurrent.futures
import csv
import datetime
import json
import os
import threading
import time
import urllib.error
import urllib.request

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from laya_ordenes_interfaces.srv import InterpretarOrden
from .logic import (analizar_laya, clasificar_respaldo, inferencia_header,
                    limpiar_catalogo, preguntas)


class InterpreteOrdenes(Node):
    def __init__(self):
        super().__init__('interprete_ordenes_logistica')
        self.declare_parameter('url_laya', '')
        self.declare_parameter('timeout_s', 2.0)
        self.declare_parameter('modelo_laya', '')
        self.declare_parameter('idioma', 'es')
        self.declare_parameter('objetos_disponibles', [''])
        self.declare_parameter('colores_disponibles', ['rojo', 'azul', 'verde', 'amarillo'])
        self.declare_parameter('confianza_minima', 0.50)
        self.declare_parameter('registro_csv', 'registro_interpretaciones.csv')
        self.declare_parameter('max_consultas', 4)
        self.url = str(self.get_parameter('url_laya').value).strip().rstrip('/')
        # El parametro timeout_s esta declarado y es visible mediante ROS 2.
        # Se lee por peticion para permitir: ros2 param set /interprete_ordenes timeout_s 3.0
        self.timeout_s = self._timeout_actual()
        self.modelo = str(self.get_parameter('modelo_laya').value).strip()
        self.idioma = str(self.get_parameter('idioma').value).strip()
        self.objetos = limpiar_catalogo(self.get_parameter('objetos_disponibles').value)
        self.colores = limpiar_catalogo(self.get_parameter('colores_disponibles').value)
        self.confianza_minima = float(self.get_parameter('confianza_minima').value)
        self.csv = str(self.get_parameter('registro_csv').value)
        self.lock_csv = threading.Lock()
        # Crear el directorio de evidencias, incluso si no existia.
        if self.csv:
            os.makedirs(os.path.dirname(os.path.abspath(self.csv)), exist_ok=True)
        limite = max(1, int(self.get_parameter('max_consultas').value))
        self.cupos = threading.BoundedSemaphore(limite)
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=limite)
        self.create_service(InterpretarOrden, '/interpretar_orden', self.interpretar,
                            callback_group=ReentrantCallbackGroup())
        self.get_logger().info(
            f'Servicio /interpretar_orden listo. URL={self.url or "NO CONFIGURADA"}, '
            f'timeout={self.timeout_s:.2f}s, inventario={self.objetos}. No mueve el brazo.')
        if not self.objetos:
            self.get_logger().warn('Inventario vacío: no se autorizarán movimientos.')

    def _timeout_actual(self):
        """Tiempo limite en segundos, configurable con un parametro ROS 2."""
        valor = float(self.get_parameter('timeout_s').value)
        if not 0.1 <= valor <= 120.0:
            raise ValueError('timeout_s debe estar entre 0.1 y 120.0 segundos')
        return valor

    def _http(self, frase, timeout_s):
        payload = {'state': frase, 'questions': preguntas(self.objetos, self.colores)}
        if self.modelo:
            payload['model'] = self.modelo
        if self.idioma:
            payload['lang'] = self.idioma
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        token = os.environ.get('LAYA_API_KEY', '').strip()
        if token:
            headers['Authorization'] = 'Bearer ' + token
        req = urllib.request.Request(self.url + '/v1/systemone', data=data,
                                     headers=headers, method='POST')
        inicio = time.perf_counter()
        # urllib timeout acota cada operación de socket. El future de abajo
        # añade un límite de tiempo total en el callback de ROS.
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            body = r.read(1024 * 1024)
            ms_inferencia = inferencia_header(r.headers)
        rtt = (time.perf_counter() - inicio) * 1000.0
        respuesta = json.loads(body.decode('utf-8'))
        return respuesta, rtt, ms_inferencia

    def _consulta_acotada(self, frase):
        timeout_s = self._timeout_actual()
        if not self.url.startswith(('http://', 'https://')):
            raise ValueError('url_laya no configurada: usar http://IP_WINDOWS:PUERTO')
        if not self.cupos.acquire(blocking=False):
            raise TimeoutError('sin cupos HTTP; servidor saturado')

        def trabajo():
            try:
                return self._http(frase, timeout_s)
            finally:
                self.cupos.release()

        try:
            futuro = self.pool.submit(trabajo)
        except Exception:
            self.cupos.release()
            raise
        try:
            return futuro.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError as exc:
            futuro.cancel()
            raise TimeoutError(f'LAYA superó timeout_s={timeout_s:.2f}') from exc

    def interpretar(self, solicitud, respuesta):
        frase = solicitud.frase.strip()
        inicio = time.perf_counter()
        rtt = -1.0
        inferencia = -1.0
        degradada = False
        fuente = 'LAYA'
        if not frase:
            degradada = True
            fuente = 'respaldo'
            decision = clasificar_respaldo(frase, self.objetos, self.colores)
            decision['motivo'] = 'frase vacía'
        else:
            try:
                respuesta_http, rtt, inferencia = self._consulta_acotada(frase)
                decision = analizar_laya(respuesta_http, frase, self.objetos, self.colores,
                                        self.confianza_minima)
            except Exception as e:
                degradada = True
                fuente = 'respaldo'
                decision = clasificar_respaldo(frase, self.objetos, self.colores)
                decision['motivo'] = f'modo degradado ({type(e).__name__}: {e}); ' + decision['motivo']
                self.get_logger().warn(decision['motivo'][:300])

        respuesta.accion = decision['accion']
        respuesta.objeto = decision['objeto']
        respuesta.color = decision['color']
        respuesta.prioridad = int(decision['prioridad'])
        respuesta.permitido = bool(decision['permitido'])
        respuesta.degradada = degradada
        respuesta.fuente = fuente
        respuesta.motivo = decision['motivo']
        respuesta.latencia_http_ms = float(rtt)
        respuesta.inferencia_ms = float(inferencia)
        # El resto incluye red + cola del servidor + serialización; NO es solo red.
        respuesta.resto_http_ms = max(0.0, rtt - inferencia) if rtt >= 0 and inferencia >= 0 else -1.0
        self._guardar(frase, respuesta, (time.perf_counter() - inicio) * 1000.0)
        return respuesta

    def _guardar(self, frase, resp, total_ms):
        if not self.csv:
            return
        try:
            with self.lock_csv:
                nuevo = not os.path.exists(self.csv) or os.path.getsize(self.csv) == 0
                with open(self.csv, 'a', newline='', encoding='utf-8') as f:
                    w = csv.writer(f)
                    if nuevo:
                        w.writerow(['fecha', 'frase', 'accion', 'objeto', 'color', 'prioridad',
                                    'permitido', 'degradada', 'fuente', 'motivo',
                                    'latencia_http_ms', 'inferencia_ms', 'resto_http_ms',
                                    'latencia_servicio_ms'])
                    w.writerow([datetime.datetime.now().isoformat(timespec='milliseconds'),
                                frase, resp.accion, resp.objeto, resp.color, resp.prioridad,
                                resp.permitido, resp.degradada, resp.fuente, resp.motivo,
                                resp.latencia_http_ms, resp.inferencia_ms,
                                resp.resto_http_ms, round(total_ms, 3)])
        except OSError as exc:
            self.get_logger().warn(f'No pude escribir CSV: {exc}')

    def destroy_node(self):
        self.pool.shutdown(wait=False, cancel_futures=True)
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    nodo = InterpreteOrdenes()
    exe = MultiThreadedExecutor(num_threads=8)
    exe.add_node(nodo)
    try:
        exe.spin()
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
