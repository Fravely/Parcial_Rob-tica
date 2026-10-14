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


if __name__ == '__main__':
    unittest.main()
