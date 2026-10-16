"""Cinemática directa del JetCobot (MyCobot 280) — ítem 1.

Convención: DH ESTÁNDAR. Cada fila de DH es (alpha_rad, a_mm, d_mm, theta_offset_rad) y la
matriz de cada eslabón es la de _t(). Tabla y matriz van de la mano: no mezcles esta tabla
con una matriz de DH modificada (la de Craig) ni al revés.
"""

import math

JOINT_NAMES = ['1_Joint', '2_Joint', '3_Joint', '4_Joint', '5_Joint', '6_Joint']

DH = [
    (math.pi / 2.0,   0.0,    132.5,    0.0),
    (0.0,            -111.5,  0.0,     -math.pi / 2.0),
    (0.0,            -95.0,   0.0,      0.0),
    (math.pi / 2.0,   0.0,    65.5,    -math.pi / 2.0),
    (-math.pi / 2.0,  0.0,    74.0,     math.pi / 2.0),
    (0.0,             0.0,    49.5,     0.0),
]

JOINT_LIMITS = [
    (-2.93, 2.93),
    (-2.36, 2.36),
    (-2.53, 2.53),
    (-2.58, 2.58),
    (-2.93, 2.93),
    (-3.14, 3.14),
]

ALCANCE_MIN_MM = 80.0
ALCANCE_MAX_MM = 480.0


def _t(alpha, a, d, theta):
    """Transformación homogénea 4x4 de un eslabón (DH estándar)."""
    ca, sa = math.cos(alpha), math.sin(alpha)
    ct, st = math.cos(theta), math.sin(theta)
    return [
        [ct,  -st * ca,   st * sa,  a * ct],
        [st,   ct * ca,  -ct * sa,  a * st],
        [0.0,  sa,        ca,       d],
        [0.0,  0.0,       0.0,      1.0],
    ]


def _mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def fk_matriz(q):
    """Matriz homogénea 4x4 de la base al efector final. q en radianes (6 valores)."""
    if len(q) != 6:
        raise ValueError(f'se esperaban 6 ángulos, llegaron {len(q)}')
    T = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for (alpha, a, d, off), theta in zip(DH, q):
        T = _mul(T, _t(alpha, a, d, theta + off))
    return T


def fk(q):
    """Posición (x, y, z) del efector final en mm, respecto a la base."""
    T = fk_matriz(q)
    x = T[0][3]
    y = T[1][3]
    z = T[2][3]
    return x, y, z


def dentro_de_limites(q):
    if len(q) != 6:
        return False, f'se esperaban 6 ángulos, llegaron {len(q)}'
    for i, (valor, (lo, hi)) in enumerate(zip(q, JOINT_LIMITS)):
        if not lo <= valor <= hi:
            return False, f'{JOINT_NAMES[i]} fuera de rango: {valor:.3f} rad, límite [{lo}, {hi}]'
    return True, ''


def dentro_del_workspace(q):
    x, y, z = fk(q)
    r = math.sqrt(x * x + y * y + z * z)
    if r > ALCANCE_MAX_MM:
        return False, f'efector a {r:.0f} mm de la base, máximo {ALCANCE_MAX_MM:.0f}'
    if r < ALCANCE_MIN_MM:
        return False, f'efector a {r:.0f} mm de la base, demasiado cerca'
    if z < 0.0:
        return False, f'z = {z:.0f} mm: el efector quedaría bajo la base'
    return True, ''


def paso_articular(q_desde, q_hasta):
    return max(abs(b - a) for a, b in zip(q_desde, q_hasta))
