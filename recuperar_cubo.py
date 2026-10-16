"""Recuperacion independiente: escaneo -> deposito -> abrir, sin pedidos ni camara.

Solo con el broker DETENIDO y MoveIt abierto:
    source scripts/entorno.sh && python3 recuperar_cubo.py --ejecutar
"""
from pathlib import Path
import argparse
import signal
import threading
import sys

def secuencia(brazo, plan, config, cancelar, radianes):
    for nombre, clave in [('ESCANEO', 'escaneo_grados'), ('DEPOSITO', 'deposito_grados')]:
        brazo.comprobar(cancelar)
        print('RECUPERACION: PLAN_' + nombre, flush=True)
        trayectoria, _, _ = plan.planificar_referencia(
            radianes(config[clave]), brazo.leer(), cancelar, lambda m: print(m, flush=True))
        print('RECUPERACION: MOVER_' + nombre, flush=True)
        brazo.ejecutar_plan(trayectoria, cancelar)
    brazo.comprobar(cancelar)
    print('RECUPERACION: SOLTAR_EN_DEPOSITO', flush=True)
    brazo.pinza(config['pinza_abierta'], cancelar)
    print('RECUPERACION TERMINADA. Comprueba que el cubo quedo en el deposito.', flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ejecutar', action='store_true',
                        help='Mueve el brazo y abre la pinza solo tras llegar al deposito.')
    args = parser.parse_args()
    if not args.ejecutar:
        parser.print_help()
        return 0
    raiz = Path(__file__).resolve().parent
    # Usa exactamente el archivo actualizado, aunque el build no fuese symlink.
    sys.path.insert(0, str(raiz / 'src/arm_broker'))
    import yaml
    import rclpy
    from rclpy.node import Node
    from rclpy.executors import MultiThreadedExecutor
    from rclpy.signals import SignalHandlerOptions
    from sensor_msgs.msg import JointState
    from arm_broker.broker import BrazoSerial, Planificador, cargar_montaje, radianes, JOINT_NAMES
    config = cargar_montaje(str(raiz / 'config/poses.json'), fisico=True)
    params = yaml.safe_load((raiz/'config/broker.yaml').read_text())['/**']['ros__parameters']
    parar = threading.Event()
    rclpy.init(signal_handler_options=SignalHandlerOptions.NO)
    signal.signal(signal.SIGINT, lambda *_: parar.set())
    signal.signal(signal.SIGTERM, lambda *_: parar.set())
    nodo = Node('recuperar_cubo', namespace='logistica')
    publicador = nodo.create_publisher(JointState, '/logistica/arm/measured_joint_states', 10)
    def publicar(q):
        msg = JointState()
        msg.header.stamp = nodo.get_clock().now().to_msg()
        msg.header.frame_id = params['moveit_marco']
        msg.name = list(JOINT_NAMES)
        msg.position = list(q)
        publicador.publish(msg)
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(nodo)
    hilo = threading.Thread(target=executor.spin, daemon=True)
    hilo.start()
    brazo = None
    try:
        plan = Planificador(nodo, grupo=params['moveit_grupo'],
                            enlace=params['moveit_enlace'], marco=params['moveit_marco'],
                            timeout=params.get('moveit_timeout_s', 8.0))
        # Este hilo es el unico propietario serial. El executor solo atiende ROS.
        brazo = BrazoSerial(config, publicar)
        secuencia(brazo, plan, config, parar.is_set, radianes)
        return 0
    except Exception as exc:
        print('RECUPERACION DETENIDA: ' + str(exc), flush=True)
        if brazo is not None:
            try: brazo.detener()
            except Exception as stop_exc: print('Error al detener: ' + str(stop_exc), flush=True)
        print('No se abre la pinza automaticamente tras el fallo.', flush=True)
        return 1
    finally:
        if brazo is not None:
            try: brazo.close()
            except Exception as exc: print('Error al cerrar puerto: ' + str(exc), flush=True)
        executor.shutdown()
        hilo.join(timeout=2)
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    raise SystemExit(main())
