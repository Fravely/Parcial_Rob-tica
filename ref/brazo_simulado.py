#!/usr/bin/env python3
"""Brazo simulado: imita lo minimo de pymycobot para ENSAYAR los scripts sin robot.

NO es el firmware ni demuestra nada del reto. Su "robot real" usa la tabla DH oficial del
MyCobot 280 (distinta de la tuya unos 4-5 mm), asi que el error que veras en la simulacion
se parece a lo que pasa con el brazo de verdad. Se activa con --simular.
"""
import math

import ik_ramas as ik

fk = ik.fk

TABLA_REAL = [
    (math.pi / 2.0, 0.0, 131.22, 0.0),
    (0.0, -110.4, 0.0, -math.pi / 2.0),
    (0.0, -96.0, 0.0, 0.0),
    (math.pi / 2.0, 0.0, 63.4, -math.pi / 2.0),
    (-math.pi / 2.0, 0.0, 75.05, math.pi / 2.0),
    (0.0, 0.0, 45.6, 0.0),
]


def fkm_real(q):
    T = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for (alpha, a, d, off), th in zip(TABLA_REAL, q):
        T = fk._mul(T, fk._t(alpha, a, d, th + off))
    return T


class BrazoSimulado:
    simulado = True

    def __init__(self, *args, **kwargs):
        self.q = [0.0] * 6                      # radianes

    def power_on(self):
        pass

    def send_angles(self, angulos_deg, velocidad):
        self.q = [math.radians(v) for v in angulos_deg]

    def send_coords(self, coords, velocidad, modo=0):
        """IK 'del firmware' (supuesto): de todas las ramas, toma la mas cercana a la pose actual."""
        T = ik.pose_T(coords[:3], ik.rpy_a_R(*coords[3:6]))
        sols = ik.buscar_soluciones(T, semillas=20, extra=[self.q], fkm=fkm_real, tol_pos=1.5)
        if sols:                                # si no hay solucion, el brazo no se mueve
            self.q = min(sols, key=lambda c: sum(abs(a - b) for a, b in zip(c, self.q)))

    def get_angles(self):
        return [round(math.degrees(v), 2) for v in self.q]

    def get_coords(self):
        T = fkm_real(self.q)
        pos = [round(T[i][3], 2) for i in range(3)]
        rpy = ik.R_a_rpy([f[:3] for f in T[:3]])
        return pos + [round(v, 2) for v in rpy]
