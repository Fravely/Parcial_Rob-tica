#!/usr/bin/env python3
"""Pruebas de la Pregunta 2 SIN ROS, sin camara y sin brazo.

Comprueba lo que se anadio al broker del RB-2:
  1) Montaje: deposito unico vs por color, poses al borde del limite articular.
  2) Admision de PickPlace: acciones admitidas, respaldo, inventario, zona.
  3) Reproduccion del plan: tolerancia intermedia vs final y fallo por tiempo.
  4) Un intento fallido (no hay cubo) NO bloquea el broker; un fallo de hardware SI.
  5) Evidencia: intentos.csv con el error del deposito y el del agarre.

NO sustituye la corrida real en el Jetson.
"""
import json
import os
import sys
import tempfile
import threading
import time
import types
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / 'src/arm_broker'))
from probar_broker_sin_ros import instalar_ros_falso, comprobar, esperar  # noqa: E402


def cargar_broker(parametros):
    for m in [k for k in sys.modules if k.startswith(('rclpy', 'sensor_msgs', 'arm_broker'))]:
        del sys.modules[m]
    reg, MoveArm = instalar_ros_falso(parametros)
    from arm_broker import broker as b
    return b, reg, MoveArm


def montaje_base(**cambios):
    c = json.loads((AQUI.parent / 'plantillas/item2_montaje.json').read_text(encoding='utf-8'))
    c['montaje_validado'] = True
    c['regiones'] = {n: [i * 110, 0, 100, 100] for i, n in
                     enumerate(('amarillo', 'azul', 'verde', 'rojo', 'deposito'))}
    c.update(cambios)
    ruta = Path(tempfile.mkdtemp()) / 'montaje.json'
    ruta.write_text(json.dumps(c), encoding='utf-8')
    return str(ruta)


def pedido(MoveArm, cliente='ana', color='rojo', accion='recoger', prioridad=80,
           fuente='LAYA', degradada=False, zona='deposito', permitido=True, objeto='cubo'):
    return MoveArm.Goal(client_id=cliente, priority=prioridad, accion=accion, objeto=objeto,
                        color=color, zona=zona, permitido=permitido, degradada=degradada,
                        fuente=fuente)


# ------------------------------------------------------------------ 1. montaje
def prueba_montaje():
    print('\n[1] Montaje: deposito y margenes articulares')
    b, _, _ = cargar_broker({})
    avisos = []
    c = b.cargar_montaje(montaje_base(), fisico=True, avisar=avisos.append)
    comprobar(set(c['_deposito']) == set(b.COLORES), 'deposito unico se copia a los 4 colores')
    comprobar(any('chocara' in a for a in avisos), 'avisa que un solo deposito hace chocar los cubos')
    comprobar(any('limite' in a and '3_Joint' in a for a in avisos),
              'avisa que la pose de deposito tiene 3_Joint al borde: ' +
              next((a for a in avisos if '3_Joint' in a), 'SIN AVISO'))

    avisos = []
    porcolor = {k: [10, -117, 85, -46, 3, -27] for k in b.COLORES}
    porcolor['rojo'] = [20, -117, 85, -46, 3, -27]
    ruta = montaje_base(deposito_grados=porcolor,
                        regiones={n: [(i % 4) * 150, (i // 4) * 200, 100, 100]
                                  for i, n in enumerate(
                                      ('amarillo', 'azul', 'verde', 'rojo', 'deposito_amarillo',
                                       'deposito_azul', 'deposito_verde', 'deposito_rojo'))})
    c = b.cargar_montaje(ruta, fisico=True, avisar=avisos.append)
    comprobar(c['_deposito']['rojo'][0] == 20 and c['_deposito']['azul'][0] == 10,
              'deposito por color conserva una pose distinta por cubo')
    comprobar(c['_region_deposito']['rojo'] == 'deposito_rojo',
              'cada color mira su propia region de deposito')
    comprobar(not any('chocara' in a for a in avisos), 'con deposito por color no avisa de choque')

    try:
        b.cargar_montaje(montaje_base(regiones={}), fisico=True)
        comprobar(False, 'sin regiones deberia fallar en modo fisico')
    except ValueError as exc:
        comprobar('regiones' in str(exc), 'sin regiones no arranca el modo fisico: ' + str(exc))
    try:
        b.cargar_montaje(montaje_base(montaje_validado=False), fisico=True)
        comprobar(False, 'montaje sin validar deberia fallar')
    except ValueError as exc:
        comprobar('pendiente' in str(exc), 'montaje sin validar no arranca: ' + str(exc))


# ------------------------------------------------------------------ 2. admision
def prueba_admision_pick():
    print('\n[2] Admision de PickPlace')
    arch = tempfile.mktemp(suffix='.csv')
    b, reg, M = cargar_broker({'habilitar_pick_place_simulado': True,
                               'inventario_pick_place': ['cubo:rojo', 'cubo:azul'],
                               'archivo_rechazos': arch, 'duracion_etapa_simulada_s': 0.0})
    nodo = b.ArmBroker()
    srv = reg.servidores[1]
    casos = [
        ('orden permitida (recoger)', pedido(M), True, ''),
        ('orden permitida (colocar)', pedido(M, accion='colocar'), True, ''),
        ('orden NO permitida', pedido(M, permitido=False), False, 'no permitida'),
        ('accion no admitida', pedido(M, accion='detener'), False, 'no admitida'),
        ('objeto fuera de inventario', pedido(M, color='verde'), False, 'inventario'),
        ('zona desconocida', pedido(M, zona='mesa'), False, 'zona'),
        ('respaldo sin habilitar', pedido(M, fuente='respaldo', degradada=True), False, 'respaldo'),
        ('fuente incoherente', pedido(M, fuente='respaldo', degradada=False), False, 'inconsistentes'),
    ]
    for nombre, g, esperado, texto in casos:
        reg.logs.clear()
        gh = srv.enviar(g)
        motivos = [m for n, m in reg.logs if n == 'WARN']
        if esperado:
            comprobar(gh is not None, nombre + ': aceptada')
        else:
            comprobar(gh is None and motivos and texto in motivos[0],
                      nombre + ': ' + (motivos[0] if motivos else 'SIN MOTIVO'))
    comprobar(esperar(lambda: nodo.n_rechazados == 6), 'se contaron los 6 rechazos')
    comprobar(Path(arch).exists() and 'no permitida' in Path(arch).read_text(encoding='utf-8'),
              'cada rechazo queda escrito con su motivo en el CSV')
    nodo.destroy_node()


# ------------------------------------------------------------------ 3. plan
class BrazoFalso:
    """MyCobot de mentira: cuenta las esperas y simula el asentamiento del brazo."""

    def __init__(self, asentar=2, fallar_en=None):
        self.q = [0.0] * 6
        self.destino = None
        self.restantes = 0
        self.asentar = asentar
        self.fallar_en = fallar_en
        self.lecturas = 0
        self.enviados = []
        self.pinza_valores = []
        self.parado = False

    def get_angles(self):
        self.lecturas += 1
        if self.restantes > 0:
            self.restantes -= 1
            return [v + 5.0 for v in self.destino]     # aun lejos
        return list(self.destino if self.destino is not None else self.q)

    def send_angles(self, grados, velocidad):
        self.enviados.append(list(grados))
        if self.fallar_en is not None and len(self.enviados) == self.fallar_en:
            return -1
        self.destino = list(grados)
        self.restantes = self.asentar
        return 1

    def is_moving(self):
        return 1 if self.restantes > 0 else 0

    def set_gripper_value(self, valor, velocidad):
        self.pinza_valores.append(valor)
        return 1

    def is_gripper_moving(self):
        return 0

    def stop(self):
        self.parado = True
        return 1

    def close(self):
        pass


def trayectoria_falsa(puntos, nombres):
    return types.SimpleNamespace(
        joint_names=list(nombres),
        points=[types.SimpleNamespace(positions=list(p)) for p in puntos])


def prueba_reproduccion_plan():
    print('\n[3] Reproduccion del plan: tolerancias y fallo por tiempo')
    b, _, _ = cargar_broker({})
    cfg = b.cargar_montaje(montaje_base())
    brazo = object.__new__(b.BrazoSerial)
    brazo.c = cfg
    brazo.telemetria = lambda q: None
    brazo.mc = BrazoFalso(asentar=1)
    import math
    base = [math.radians(v) for v in cfg['escaneo_grados']]
    puntos = [base, [v + 0.02 for v in base], [v + 0.04 for v in base], [v + 0.06 for v in base]]
    brazo.mc.destino = [math.degrees(v) for v in base]
    final = brazo.ejecutar_plan(trayectoria_falsa(puntos, b.JOINT_NAMES), lambda: False)
    comprobar(len(brazo.mc.enviados) == 3, 'se envian TODOS los puntos del plan, no solo el final')
    comprobar(abs(final[0] - puntos[-1][0]) < 1e-6, 'devuelve la lectura real del ultimo punto')

    brazo.mc = BrazoFalso(asentar=1)
    brazo.mc.destino = [math.degrees(v) for v in base]
    cfg_lento = dict(cfg, timeout_movimiento_s=1, tolerancia_intermedia_grados=0.1,
                     tolerancia_articular_grados=0.1)
    brazo.c = cfg_lento
    brazo.mc.asentar = 10 ** 6          # nunca llega
    try:
        brazo.ejecutar_plan(trayectoria_falsa(puntos, b.JOINT_NAMES), lambda: False)
        comprobar(False, 'un brazo que no llega deberia dar ErrorDeHardware')
    except b.ErrorDeHardware as exc:
        comprobar('no alcanzo el punto' in str(exc), 'brazo que no llega: ' + str(exc)[:70])

    brazo.c = cfg
    brazo.mc = BrazoFalso(asentar=1, fallar_en=2)
    brazo.mc.destino = [math.degrees(v) for v in base]
    try:
        brazo.ejecutar_plan(trayectoria_falsa(puntos, b.JOINT_NAMES), lambda: False)
        comprobar(False, 'un punto rechazado deberia dar ErrorDeHardware')
    except b.ErrorDeHardware as exc:
        comprobar('rechazo el punto' in str(exc), 'controlador que rechaza: ' + str(exc)[:70])

    brazo.mc = BrazoFalso(asentar=1)
    brazo.mc.destino = [math.degrees(v) for v in base]
    try:
        brazo.ejecutar_plan(trayectoria_falsa([base, [v + 1.0 for v in base]], b.JOINT_NAMES),
                            lambda: False)
        comprobar(False, 'un plan con saltos enormes deberia rechazarse')
    except b.ErrorDePedido as exc:
        comprobar('disperso' in str(exc), 'plan demasiado disperso: ' + str(exc)[:60])


# ------------------------------------------------------------------ 4 y 5
class PlanificadorFalso:
    def __init__(self, *a, **kw):
        self.validaciones = 0

    def validar_modelo_rb2(self, referencias, cancelado):
        self.validaciones += 1

    def planificar_referencia(self, referencia, actual, cancelado, feedback, altura=0.0):
        feedback('IK_MOVEIT2_SOLO_PLAN')
        feedback('TRAYECTORIA_MOVEIT2_SOLO_PLAN')
        import arm_broker.broker as b
        destino = list(referencia)
        if altura:
            destino = [v + 0.01 for v in referencia]
        return (trayectoria_falsa([actual, destino], b.JOINT_NAMES),
                ['IK_MOVEIT2_SOLO_PLAN', 'TRAYECTORIA_MOVEIT2_SOLO_PLAN'], [0.01, 0.02])


class VisionFalsa:
    """hay_cubo / deposito_lleno se cambian entre intentos."""
    hay_cubo = True
    entrego = True

    def __init__(self, config):
        self.c = config

    def observar(self, color, cancelado, carpeta, etiqueta):
        Path(carpeta).mkdir(parents=True, exist_ok=True)
        grande = [5000.0] * 3
        chico = [0.0] * 3
        if etiqueta == 'antes':
            return {'origen_areas': grande if VisionFalsa.hay_cubo else chico,
                    'deposito_areas': chico}
        return {'origen_areas': chico,
                'deposito_areas': grande if VisionFalsa.entrego else chico}


def crear_broker_fisico(extra=None):
    carpeta = tempfile.mkdtemp()
    parametros = {'habilitar_pick_place_fisico': True, 'config_item2': montaje_base(),
                  'inventario_pick_place': ['cubo:rojo', 'cubo:azul'],
                  'evidencias_item2': carpeta + '/item2',
                  'archivo_rechazos': carpeta + '/rechazos.csv',
                  'politica': 'prioridad'}
    parametros.update(extra or {})
    b, reg, M = cargar_broker(parametros)
    b.Planificador = PlanificadorFalso
    b.VisionFija = VisionFalsa
    falsos = {}

    class BrazoPatch:
        def __init__(self, config, telemetria):
            self.c = config
            self.telemetria = telemetria
            self.mc = BrazoFalso(asentar=0)
            import math
            self.mc.destino = list(config['escaneo_grados'])
            falsos['brazo'] = self
            if falsos.get('romper'):
                raise b.ErrorDeHardware(falsos['romper'])

        def leer(self):
            import math
            q = [math.radians(v) for v in self.mc.destino]
            self.telemetria(q)
            return q

        def ejecutar_plan(self, trayectoria, cancelado):
            import math
            ultimo = trayectoria.points[-1].positions
            self.mc.destino = [math.degrees(v) for v in ultimo]
            if falsos.get('romper_mover'):
                raise b.ErrorDeHardware(falsos['romper_mover'])
            return list(ultimo)

        def pinza(self, valor, cancelado):
            self.mc.pinza_valores.append(valor)

        def detener(self):
            self.mc.parado = True

        def close(self):
            pass

    b.BrazoSerial = BrazoPatch
    nodo = b.ArmBroker()
    return b, reg, M, nodo, reg.servidores[1], carpeta, falsos


def prueba_fallos_no_bloquean():
    print('\n[4] Un intento fallido no bloquea el broker; un fallo de hardware si')
    VisionFalsa.hay_cubo, VisionFalsa.entrego = True, True
    b, reg, M, nodo, srv, carpeta, falsos = crear_broker_fisico()

    gh = srv.enviar(pedido(M, cliente='ana', color='rojo'))
    comprobar(gh is not None and esperar(lambda: gh.terminado.is_set()), 'intento 1 termina')
    comprobar(gh.resultado.success and gh.resultado.physical_verified,
              'intento 1 exitoso y verificado por vision')
    comprobar(gh.resultado.position_error_mm >= 0, 'intento 1 informa el error del deposito')

    VisionFalsa.hay_cubo = False                      # el docente retira el cubo
    gh2 = srv.enviar(pedido(M, cliente='luis', color='rojo'))
    comprobar(gh2 is not None and esperar(lambda: gh2.terminado.is_set()), 'intento 2 termina')
    comprobar(not gh2.resultado.success and 'no esta' in gh2.resultado.message,
              'sin cubo: intento fallido con motivo legible')
    comprobar(nodo.fallo_fisico == '', 'un cubo ausente NO enclava el broker')

    VisionFalsa.hay_cubo = True
    gh3 = srv.enviar(pedido(M, cliente='eva', color='azul'))
    comprobar(gh3 is not None and esperar(lambda: gh3.terminado.is_set()),
              'el broker sigue aceptando pedidos despues del fallo')
    comprobar(gh3.resultado.success, 'intento 3 exitoso tras el fallo anterior')

    VisionFalsa.entrego = False                       # el cubo no aparece en el deposito
    gh4 = srv.enviar(pedido(M, cliente='tom', color='rojo'))
    esperar(lambda: gh4.terminado.is_set())
    comprobar(not gh4.resultado.success and not gh4.resultado.physical_verified,
              'entrega no confirmada: intento fallido, no exito')
    comprobar(nodo.fallo_fisico == '', 'una entrega no confirmada tampoco enclava')
    VisionFalsa.entrego = True

    falsos['romper_mover'] = 'el brazo no confirmo la llegada'
    gh5 = srv.enviar(pedido(M, cliente='ana', color='rojo'))
    esperar(lambda: gh5.terminado.is_set())
    comprobar(not gh5.resultado.success and 'FALLO DE HARDWARE' in gh5.resultado.message,
              'fallo de hardware: el intento falla y se avisa')
    comprobar(nodo.fallo_fisico != '', 'un fallo de hardware SI enclava el broker')
    comprobar(falsos['brazo'].mc.parado, 'ante el fallo se ordena la parada del brazo')

    reg.logs.clear()
    gh6 = srv.enviar(pedido(M, cliente='luis', color='rojo'))
    motivos = [m for n, m in reg.logs if n == 'WARN']
    comprobar(gh6 is None and motivos and 'enclavado' in motivos[0],
              'con el broker enclavado se rechaza con motivo: ' +
              (motivos[0][:60] if motivos else 'SIN MOTIVO'))

    print('\n[5] Evidencia de los intentos')
    csv_intentos = Path(carpeta) / 'item2/intentos.csv'
    comprobar(csv_intentos.exists(), 'se escribio intentos.csv')
    import csv as _csv
    filas = list(_csv.DictReader(csv_intentos.open(encoding='utf-8')))
    comprobar(len(filas) == 5, f'quedan los 5 intentos fisicos, con fallos incluidos ({len(filas)})')
    comprobar([f['success'] for f in filas] == ['True', 'False', 'True', 'False', 'False'],
              'el CSV conserva exitos y fallos tal cual')
    comprobar(float(filas[0]['error_agarre_mm']) >= 0, 'el CSV trae el error FK del agarre')
    comprobar(float(filas[0]['position_error_mm']) >= 0, 'el CSV trae el error FK del deposito')
    comprobar(filas[0]['accion'] == 'recoger' and filas[0]['fuente'] == 'LAYA',
              'el CSV guarda accion y fuente de la decision')
    detalle = Path(carpeta) / 'item2' / filas[0]['goal_id'] / 'intento.json'
    comprobar(detalle.exists(), 'cada goal deja su intento.json con el detalle')
    nodo.destroy_node()


def prueba_colocar_y_prioridad():
    print('\n[6] La prioridad del modelo decide el orden; colocar tambien se atiende')
    VisionFalsa.hay_cubo, VisionFalsa.entrego = True, True
    b, reg, M, nodo, srv, carpeta, falsos = crear_broker_fisico()
    manejadores = []
    for cliente, prio, accion in (('ana', 10, 'recoger'), ('luis', 200, 'colocar'),
                                  ('eva', 50, 'recoger')):
        manejadores.append(srv.enviar(pedido(M, cliente=cliente, prioridad=prio, accion=accion)))
        time.sleep(0.02)
    comprobar(all(h is not None for h in manejadores), 'los tres entran, incluido colocar')
    comprobar(esperar(lambda: all(h.terminado.is_set() for h in manejadores), 30),
              'los tres terminan')
    import csv as _csv
    filas = list(_csv.DictReader((Path(carpeta) / 'item2/intentos.csv').open(encoding='utf-8')))
    orden = [f['cliente'] for f in filas]
    comprobar(orden[0] == 'ana', 'el primero en llegar ya se estaba ejecutando: ' + str(orden))
    comprobar(orden[1] == 'luis', 'de los que esperaban, sale antes la prioridad 200: ' + str(orden))
    nodo.destroy_node()


def prueba_vision_pura():
    print('\n[7] Criterio de verificacion por vision')
    b, _, _ = cargar_broker({})
    lleno, vacio = [5000.0] * 3, [0.0] * 3
    comprobar(b.verificar_deposito({'origen_areas': lleno, 'deposito_areas': vacio},
                                   {'origen_areas': vacio, 'deposito_areas': lleno}, 1000),
              'origen se vacia y deposito se llena: entrega verificada')
    comprobar(not b.verificar_deposito({'origen_areas': lleno, 'deposito_areas': lleno},
                                       {'origen_areas': vacio, 'deposito_areas': lleno}, 1000),
              'si el deposito YA tenia ese color, no cuenta como entrega nueva')
    comprobar(not b.verificar_deposito({'origen_areas': lleno, 'deposito_areas': vacio},
                                       {'origen_areas': lleno, 'deposito_areas': lleno}, 1000),
              'si el cubo sigue en el origen, no cuenta')


def main():
    prueba_montaje()
    prueba_admision_pick()
    prueba_reproduccion_plan()
    prueba_fallos_no_bloquean()
    prueba_colocar_y_prioridad()
    prueba_vision_pura()
    print('\n' + ('TODO OK' if comprobar.fallos == 0 else f'{comprobar.fallos} FALLOS'))
    return 1 if comprobar.fallos else 0


if __name__ == '__main__':
    sys.exit(main())
