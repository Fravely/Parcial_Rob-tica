#!/usr/bin/env python3
"""Prueba la LÓGICA del broker sin ROS 2 ni brazo: sustituye rclpy por un doble de prueba.

    python3 probar_broker_sin_ros.py

Qué comprueba:
  1) Admisión: cada rechazo trae un motivo legible y se cuentan aceptados/rechazados.
  2) Exclusión mutua: con 4 clientes a la vez, nunca hay dos ejecuciones solapadas y los
     mensajes de /joint_states de cada pedido salen en un bloque contiguo.
  3) FIFO: se atiende en orden de llegada. Prioridad con envejecimiento: nadie se queda sin turno.
  4) Cancelación en cola: el goal se cierra y el worker no se atasca.

IMPORTANTE: es un modelo. NO sustituye la corrida con ROS 2 real: la evidencia del reto
(ros2 bag, logs, `Publisher count: 1`) sale del Jetson, no de este script.
"""
import os
import sys
import tempfile
import threading
import time
import types

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'src', 'arm_broker'))


# ----------------------------------------------------------------- doble de ROS 2
class _Plano:
    """Mensaje genérico: acepta cualquier atributo."""
    def __init__(self, **kw):
        self.__dict__.update(kw)


def instalar_ros_falso(parametros):
    reg = types.SimpleNamespace(joint=[], logs=[], lock=threading.Lock(), servidores=[])

    class GoalResponse:
        ACCEPT, REJECT = 'ACCEPT', 'REJECT'

    class CancelResponse:
        ACCEPT, REJECT = 'ACCEPT', 'REJECT'

    class Grupo:
        pass

    class Logger:
        def _l(self, nivel, m):
            with reg.lock:
                reg.logs.append((nivel, m))

        def info(self, m, **kw): self._l('INFO', m)
        def warn(self, m, **kw): self._l('WARN', m)
        def error(self, m, **kw): self._l('ERROR', m)

    class Pub:
        def __init__(self, topico): self.topico = topico

        def publish(self, msg):
            if self.topico == '/joint_states':
                reg.joint.append(msg)

    class Reloj:
        def now(self): return self
        def to_msg(self): return None

    class Param:
        def __init__(self, v): self.value = v

    class Node:
        def __init__(self, nombre):
            self._p = {}
            self._log = Logger()

        def get_logger(self): return self._log
        def declare_parameter(self, n, d): self._p[n] = parametros.get(n, d)
        def get_parameter(self, n): return Param(self._p[n])
        def create_publisher(self, tipo, topico, qos): return Pub(topico)
        def get_clock(self): return Reloj()
        def destroy_node(self): pass

        def create_timer(self, periodo, cb, callback_group=None):
            def lazo():
                while True:
                    time.sleep(periodo)
                    cb()
            threading.Thread(target=lazo, daemon=True).start()

    class Manejador:
        """Hace de ServerGoalHandle."""
        def __init__(self, servidor, goal):
            self.request = goal
            self.goal_id = types.SimpleNamespace(uuid=os.urandom(16))
            self.cancelando = False
            self.estado = 'ACCEPTED'
            self.resultado = None
            self.terminado = threading.Event()
            self._servidor = servidor

        @property
        def is_cancel_requested(self): return self.cancelando

        def execute(self):
            def correr():
                self.resultado = self._servidor.execute_callback(self)
                self.terminado.set()
            threading.Thread(target=correr, daemon=True).start()

        def succeed(self): self.estado = 'SUCCEEDED'
        def abort(self): self.estado = 'ABORTED'

        def canceled(self):
            self.estado = 'CANCELED'
            if self.resultado is None:
                self.resultado = _Plano(success=False, message='cancelado en cola')
            self.terminado.set()

        def publish_feedback(self, fb): pass

        def cancelar(self): self.cancelando = True

    class ActionServer:
        def __init__(self, nodo, tipo, nombre, goal_callback, handle_accepted_callback,
                     cancel_callback, execute_callback, callback_group=None):
            self.goal_callback = goal_callback
            self.handle_accepted_callback = handle_accepted_callback
            self.execute_callback = execute_callback
            reg.servidores.append(self)

        def enviar(self, goal):
            """Imita al cliente: devuelve el manejador, o None si el portero rechazó."""
            if self.goal_callback(goal) != GoalResponse.ACCEPT:
                return None
            gh = Manejador(self, goal)
            self.handle_accepted_callback(gh)
            return gh

    class MoveArm:
        Goal = Result = Feedback = _Plano

    def modulo(nombre, **attrs):
        m = types.ModuleType(nombre)
        m.__dict__.update(attrs)
        sys.modules[nombre] = m
        return m

    modulo('rclpy', ok=lambda: True, init=lambda args=None: None, shutdown=lambda: None)
    modulo('rclpy.action', ActionServer=ActionServer, CancelResponse=CancelResponse,
           GoalResponse=GoalResponse)
    modulo('rclpy.callback_groups', MutuallyExclusiveCallbackGroup=Grupo,
           ReentrantCallbackGroup=Grupo)
    modulo('rclpy.executors', MultiThreadedExecutor=object)
    modulo('rclpy.node', Node=Node)
    modulo('sensor_msgs')
    modulo('sensor_msgs.msg', JointState=lambda: _Plano(header=_Plano(stamp=None, frame_id='')))
    modulo('arm_broker_interfaces')
    modulo('arm_broker_interfaces.action', MoveArm=MoveArm, PickPlace=MoveArm)
    modulo('arm_broker_interfaces.msg', QueueState=_Plano)
    return reg, MoveArm


# ----------------------------------------------------------------- utilidades de prueba
def crear_broker(parametros):
    for m in [k for k in sys.modules if k.startswith(('rclpy', 'sensor_msgs', 'arm_broker'))]:
        del sys.modules[m]
    parametros = dict(parametros, publicar_joint_states=True)  # SOLO en ROS falso, nunca hay hardware
    reg, MoveArm = instalar_ros_falso(parametros)
    from arm_broker import broker as b                       # noqa: E402
    nodo = b.ArmBroker()
    return nodo, reg, MoveArm, reg.servidores[0]


def goal(MoveArm, q, cliente, prio):
    g = MoveArm.Goal(joint_positions=list(q), client_id=cliente, priority=prio)
    return g


def esperar(cond, timeout=20.0):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if cond():
            return True
        time.sleep(0.01)
    return False


def poses_validas(n, semilla=7):
    import random
    from arm_broker import fk
    random.seed(semilla)
    rangos = [(-0.8, 0.8), (-1.0, -0.2), (0.2, 1.0), (-0.3, 0.3), (-0.5, 0.5), (-0.5, 0.5)]
    out = []
    while len(out) < n:
        q = [round(random.uniform(lo, hi), 4) for lo, hi in rangos]
        if fk.dentro_de_limites(q)[0] and fk.dentro_del_workspace(q)[0]:
            out.append(q)
    return out


def comprobar(cond, texto):
    print(('  OK   ' if cond else '  FALLA') + ' ' + texto)
    if not cond:
        comprobar.fallos += 1


comprobar.fallos = 0


# ----------------------------------------------------------------- pruebas
def prueba_admision():
    print('\n[1] Admisión: motivos de rechazo')
    arch = tempfile.mktemp(suffix='.csv')
    nodo, reg, M, srv = crear_broker({'archivo_rechazos': arch})
    casos = [
        ('fuera de límites articulares', [3.5, 0, 0, 0, 0, 0], 'límites articulares'),
        ('número de ángulos incorrecto', [0.1, 0.2], 'se esperaban 6'),
        ('fuera del workspace (muy lejos)', [0, 0, 0, 0, 0, 0], None),   # se decide abajo
        ('paso articular excesivo', [1.5, 0, 0, 0, 0, 0], 'paso articular excesivo'),
    ]
    from arm_broker import fk
    for nombre, q, esperado in casos:
        if nombre.startswith('fuera del workspace'):
            # busco una pose válida en límites pero con z < 0 o r > alcance
            q = [0.0, 1.8, 1.8, 0.0, 0.0, 0.0]
            esperado = 'workspace'
            assert fk.dentro_de_limites(q)[0], 'la pose de prueba debe respetar los límites'
        reg.logs.clear()
        gh = srv.enviar(goal(M, q, 'prueba', 3))
        motivos = [m for n, m in reg.logs if n == 'WARN']
        ok = gh is None and bool(motivos) and esperado in motivos[0]
        comprobar(ok, f'{nombre}: {motivos[0] if motivos else "SIN MOTIVO"}')
    gh = srv.enviar(goal(M, [0.3, 0, 0, 0, 0, 0], 'prueba', 3))
    comprobar(gh is not None, 'una pose válida se acepta')
    comprobar(nodo.n_rechazados == 4 and nodo.n_aceptados == 1,
              f'contadores: aceptados={nodo.n_aceptados} rechazados={nodo.n_rechazados}')
    with open(arch) as f:
        filas = f.read().strip().splitlines()
    comprobar(len(filas) == 5, f'registro_rechazos.csv tiene {len(filas) - 1} rechazos con motivo')
    gh.terminado.wait(10)
    os.remove(arch)


def correr_clientes(nodo, M, srv, poses, prios, por_cliente):
    """4 clientes a lazo cerrado, como cliente.py: envían, esperan el resultado, pausan."""
    resultados = {c: [] for c in prios}

    def cliente(c):
        for q in poses[:por_cliente]:
            gh = srv.enviar(goal(M, q, c, prios[c]))
            if gh is None:
                resultados[c].append('RECHAZADO')
                continue
            gh.terminado.wait(30)
            resultados[c].append(gh.estado)
            time.sleep(0.01)

    hilos = [threading.Thread(target=cliente, args=(c,)) for c in prios]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join(60)
    return resultados


def prueba_concurrencia(politica):
    print(f'\n[2] Cuatro clientes a la vez · política = {politica}')
    nodo, reg, M, srv = crear_broker({
        'politica': politica, 'duracion_movimiento_s': 0.08, 'pasos_interpolacion': 4,
        'paso_max_rad': 3.0, 'archivo_rechazos': ''})
    # vigilante de solapamiento: cuenta ejecuciones simultáneas de execute_callback
    estado = {'activas': 0, 'max': 0, 'inicios': []}
    original = nodo.execute_callback
    cerrojo = threading.Lock()

    def vigilado(gh):
        with cerrojo:
            estado['activas'] += 1
            estado['max'] = max(estado['max'], estado['activas'])
            estado['inicios'].append(nodo.ejecutando)
        try:
            return original(gh)
        finally:
            with cerrojo:
                estado['activas'] -= 1
    srv.execute_callback = vigilado
    # cada mensaje de /joint_states lleva anotado quién estaba ejecutando
    mover = nodo.mover

    def mover_anotado(q):
        mover(q)
        reg.joint[-1].quien = nodo.ejecutando.goal_id if nodo.ejecutando else None
    nodo.mover = mover_anotado

    poses = poses_validas(6)
    prios = {'ana': 1, 'luis': 3, 'eva': 5, 'tom': 7}
    res = correr_clientes(nodo, M, srv, poses, prios, 6)

    total = sum(len(v) for v in res.values())
    comprobar(estado['max'] == 1, f'ejecuciones simultáneas máximas = {estado["max"]} (debe ser 1)')
    ids = [m.quien for m in reg.joint]
    bloques = [ids[0]] if ids else []
    for i in ids[1:]:
        if i != bloques[-1]:
            bloques.append(i)
    comprobar(len(bloques) == len(set(bloques)),
              f'/joint_states: {len(set(bloques))} pedidos, cada uno en un bloque contiguo (sin intercalar)')
    comprobar(all(e == 'SUCCEEDED' for v in res.values() for e in v),
              f'los {total} goals terminaron SUCCEEDED')
    comprobar(nodo.n_completados == nodo.n_aceptados == total,
              f'completados={nodo.n_completados} aceptados={nodo.n_aceptados}')
    comprobar(nodo.ejecutando is None and not nodo.pendientes, 'la cola quedó vacía y el brazo libre')
    return estado, reg, nodo


def prueba_fifo_orden():
    print('\n[3] FIFO: se atiende en orden de llegada')
    nodo, reg, M, srv = crear_broker({
        'politica': 'fifo', 'duracion_movimiento_s': 0.1, 'pasos_interpolacion': 2,
        'paso_max_rad': 3.0, 'archivo_rechazos': ''})
    poses = poses_validas(8)
    mangos = []
    # el primero ocupa el brazo; los demás llegan escalonados mientras espera
    for i, q in enumerate(poses):
        mangos.append(srv.enviar(goal(M, q, f'c{i}', (i * 37) % 9)))
        time.sleep(0.003)
    for gh in mangos:
        gh.terminado.wait(20)
    orden = [m for n, m in reg.logs if n == 'INFO' and m.startswith('EJECUTANDO')]
    nombres = [m.split()[1] for m in orden]
    comprobar(nombres == [f'c{i}' for i in range(len(poses))], f'orden de ejecución: {nombres}')


def _corrida_flujo_urgente(tau):
    """Un pedido de prioridad 0 compite contra un flujo continuo de pedidos de prioridad 9."""
    nodo, reg, M, srv = crear_broker({
        'politica': 'prioridad', 'tau_envejecimiento_s': tau, 'duracion_movimiento_s': 0.1,
        'pasos_interpolacion': 2, 'paso_max_rad': 3.0, 'archivo_rechazos': ''})
    poses = poses_validas(18)
    mangos = [srv.enviar(goal(M, poses[0], 'ocupa', 9))]       # ocupa el brazo al inicio
    time.sleep(0.02)
    mangos.append(srv.enviar(goal(M, poses[1], 'baja', 0)))    # la prioridad 0 llega primero
    for i in range(2, 18):                                     # y sigue llegando gente urgente
        mangos.append(srv.enviar(goal(M, poses[i], f'alta{i}', 9)))
        time.sleep(0.06)
    for gh in mangos:
        gh.terminado.wait(30)
    orden = [m.split()[1] for n, m in reg.logs if n == 'INFO' and m.startswith('EJECUTANDO')]
    return orden.index('baja') + 1, len(orden)


def prueba_envejecimiento():
    print('\n[4] Prioridad con envejecimiento: la prioridad baja no se muere de hambre')
    lugar_est, n = _corrida_flujo_urgente(1e9)      # tau enorme = prioridad estática
    lugar_env, n = _corrida_flujo_urgente(0.05)     # (p_max - p) * tau = 0.45 s
    comprobar(lugar_est == n, f'prioridad ESTÁTICA: el pedido de prioridad 0 sale en el lugar {lugar_est} de {n} (inanición)')
    comprobar(lugar_env < n, f'con ENVEJECIMIENTO sale en el lugar {lugar_env} de {n}')


def prueba_cancelacion():
    print('\n[5] Cancelación de un goal que espera en la cola')
    nodo, reg, M, srv = crear_broker({
        'politica': 'fifo', 'duracion_movimiento_s': 0.3, 'pasos_interpolacion': 3,
        'paso_max_rad': 3.0, 'archivo_rechazos': ''})
    poses = poses_validas(3)
    g1 = srv.enviar(goal(M, poses[0], 'a', 5))
    time.sleep(0.05)
    g2 = srv.enviar(goal(M, poses[1], 'b', 5))
    g2.cancelar()
    g3 = srv.enviar(goal(M, poses[2], 'c', 5))
    ok = all(g.terminado.wait(20) for g in (g1, g2, g3))
    comprobar(ok, 'los tres goals terminaron (el worker no se atascó)')
    comprobar(g2.estado == 'CANCELED', f'el cancelado quedó {g2.estado}')
    comprobar(g3.estado == 'SUCCEEDED', f'el siguiente se ejecutó normalmente ({g3.estado})')


def prueba_paso_max_en_carga():
    print('\n[6] Aviso para el ítem 3: con paso_max por defecto algunos goals de la carga se rechazan')
    nodo, reg, M, srv = crear_broker({
        'politica': 'fifo', 'duracion_movimiento_s': 0.03, 'pasos_interpolacion': 2,
        'archivo_rechazos': ''})
    poses = poses_validas(40)
    rechazados = 0
    for q in poses:
        gh = srv.enviar(goal(M, q, 'c', 1))
        if gh is None:
            rechazados += 1
        else:
            gh.terminado.wait(10)
    print(f'  INFO con paso_max_rad=1.2 (por defecto) se rechazaron {rechazados} de {len(poses)} poses de la carga')
    print('  INFO para medir el ítem 3 usa  -p paso_max_rad:=2.0  y todas entran en ambas políticas')


if __name__ == '__main__':
    prueba_admision()
    prueba_concurrencia('fifo')
    prueba_concurrencia('prioridad')
    prueba_fifo_orden()
    prueba_envejecimiento()
    prueba_cancelacion()
    prueba_paso_max_en_carga()
    print('\n' + ('TODO OK' if comprobar.fallos == 0 else f'{comprobar.fallos} COMPROBACIONES FALLARON'))
    sys.exit(1 if comprobar.fallos else 0)
