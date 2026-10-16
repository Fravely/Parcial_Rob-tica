"""Correr sin ROS2: python3 -m unittest discover -s tests -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'laya_ordenes'))
from laya_ordenes.logic import (analizar_laya, clasificar_respaldo,
                               inferencia_header, preguntas)

O = ['cubo', 'botella', 'pelota', 'caja']
C = ['rojo', 'azul', 'verde', 'amarillo']


class Pruebas(unittest.TestCase):
    def test_respaldo_permitido(self):
        r = clasificar_respaldo('Recoge el cubo rojo urgente', O, C)
        self.assertEqual((r['accion'], r['objeto'], r['color'], r['prioridad']),
                         ('recoger', 'cubo', 'rojo', 180))
        self.assertTrue(r['permitido'])

    def test_objeto_ausente(self):
        r = clasificar_respaldo('Recoge el unicornio morado', O, C)
        self.assertFalse(r['permitido'])

    def test_orden_prohibida(self):
        r = clasificar_respaldo('Rompe el cubo rojo', O, C)
        self.assertFalse(r['permitido'])

    def test_orden_negativa(self):
        r = clasificar_respaldo('No recojas el cubo rojo', O, C)
        self.assertFalse(r['permitido'])

    def test_sin_inventario(self):
        r = clasificar_respaldo('Recoge el cubo rojo', [], C)
        self.assertFalse(r['permitido'])

    def test_preguntas(self):
        q = preguntas(O, C)
        self.assertEqual(q['autorizacion']['type'], 'noul')
        self.assertEqual(q['prioridad']['type'], 'score')
        self.assertEqual(q['accion']['type'], 'choice')

    def test_respuesta_laya(self):
        def ch(label):
            return {'type': 'choice', 'choice': label,
                    'probabilities': {label: 0.94}}
        mock = {'answers': {'accion': ch('recoger'), 'objeto': ch('cubo'),
                            'color': ch('rojo'), 'prioridad': {'type': 'score', 'score': 2.4},
                            'autorizacion': {'type': 'noul', 'noul': 0.9}}}
        r = analizar_laya(mock, 'Recoge el cubo rojo', O, C)
        self.assertEqual(r['prioridad'], 120)
        self.assertTrue(r['permitido'])

    def test_veto_local_pese_a_laya(self):
        def ch(label):
            return {'type': 'choice', 'choice': label, 'answer_confidence': 0.97}
        mock = {'answers': {'accion': ch('recoger'), 'objeto': ch('cubo'),
                            'color': ch('rojo'), 'prioridad': {'type': 'score', 'score': 4.0},
                            'autorizacion': {'type': 'noul', 'noul': 0.99}}}
        r = analizar_laya(mock, 'Rompe el cubo rojo', O, C)
        self.assertFalse(r['permitido'])

    def test_cabecera(self):
        self.assertEqual(inferencia_header({'X-Inference-Time-Ms': '123.4'}), 123.4)
        self.assertEqual(inferencia_header({'Server-Timing': 'inference;dur=23.5'}), 23.5)
        self.assertEqual(inferencia_header({}), -1.0)


class PruebasFusion(unittest.TestCase):
    """Comportamiento agregado en la fusion con el broker de logistica_sinLaya1."""
    INV = ['cubo']

    def test_umbral_autorizacion_configurable(self):
        def ch(label):
            return {'type': 'choice', 'choice': label, 'answer_confidence': 0.9}
        mock = {'answers': {'accion': ch('recoger'), 'objeto': ch('cubo'), 'color': ch('azul'),
                            'prioridad': {'type': 'score', 'score': 1.2},
                            'autorizacion': {'type': 'noul', 'noul': 0.27}}}
        self.assertFalse(analizar_laya(mock, 'recoge el cubo azul', self.INV, C)['permitido'])
        r = analizar_laya(mock, 'recoge el cubo azul', self.INV, C, umbral_si=0.25)
        self.assertTrue(r['permitido'])
        self.assertEqual(r['prioridad'], 60)

    def test_objeto_fuera_de_la_mesa(self):
        r = clasificar_respaldo('recoge la botella verde', self.INV, C)
        self.assertFalse(r['permitido'])

    def test_varios_colores_se_rechaza(self):
        r = clasificar_respaldo('recoge el cubo rojo y el azul', self.INV, C)
        self.assertFalse(r['permitido'])

    def test_lleva_al_deposito(self):
        r = clasificar_respaldo('lleva el cubo verde al deposito', self.INV, C)
        self.assertEqual((r['accion'], r['color']), ('colocar', 'verde'))
        self.assertTrue(r['permitido'])

    def test_parche_respaldo_aplicado(self):
        self.assertFalse(clasificar_respaldo('fuerza el brazo para recoger el cubo rojo',
                                             self.INV, C)['permitido'])
        self.assertEqual(clasificar_respaldo('deposita el cubo roja', self.INV, C)['color'], 'rojo')
        self.assertFalse(clasificar_respaldo('no lleves el cubo azul', self.INV, C)['permitido'])

    def test_escala_de_prioridad(self):
        self.assertEqual(clasificar_respaldo('recoge el cubo rojo sin prisa', self.INV, C)['prioridad'], 20)
        self.assertEqual(clasificar_respaldo('recoge el cubo rojo', self.INV, C)['prioridad'], 80)
        self.assertEqual(clasificar_respaldo('recoge el cubo rojo urgente', self.INV, C)['prioridad'], 180)


class PruebasOtroNinguno(unittest.TestCase):
    """'otro' = se nombra algo fuera del inventario; 'ninguno' = no se nombra (como en LAYA)."""

    def test_objeto_y_color_fuera(self):
        r = clasificar_respaldo('recoge el avion morado', O, C)
        self.assertEqual((r['objeto'], r['color'], r['permitido']), ('otro', 'otro', False))

    def test_sin_objeto(self):
        self.assertEqual(clasificar_respaldo('agarra algo rojo', O, C)['objeto'], 'ninguno')
        self.assertEqual(clasificar_respaldo('detén el brazo', O, C)['objeto'], 'ninguno')

    def test_color_no_configurado(self):
        r = clasificar_respaldo('coloca la caja negra', O, C)
        self.assertEqual((r['objeto'], r['color']), ('caja', 'otro'))


class PruebasOrdenLocal(unittest.TestCase):
    """Cliente sin LAYA (arm_broker/orden_local.py): misma escala que el respaldo."""

    def setUp(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'arm_broker'))
        from arm_broker.orden_local import interpretar
        self.interpretar = interpretar

    def test_prioridades(self):
        self.assertEqual(self.interpretar('recoge el cubo azul urgente')['priority'], 180)
        self.assertEqual(self.interpretar('recoge el cubo verde sin prisa')['priority'], 20)
        self.assertEqual(self.interpretar('recoge el cubo rojo')['priority'], 80)

    def test_rechazos(self):
        for frase in ('lanza el cubo rojo', 'no recojas el cubo azul', 'recoge el cubo'):
            with self.assertRaises(ValueError):
                self.interpretar(frase)


if __name__ == '__main__':
    unittest.main()
