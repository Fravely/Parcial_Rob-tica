#!/usr/bin/env python3
"""IK numerica (minimos cuadrados amortiguados) construida sobre TU fk.py.

NO reemplaza al firmware: el reto pide que la IK la resuelva send_coords().
Esto sirve para ANALIZAR: dado un q ejecutado por el firmware, encuentra las otras
configuraciones (ramas, p. ej. el codo contrario) que alcanzan la MISMA pose del
efector, y las compara con la que el brazo eligio.

Puro Python (sin numpy), para que corra igual en el Jetson, la Raspberry o tu PC.

Uso suelto (re-analizar un JSON guardado por auditar_ik.py, sin robot):
    python3 ik_ramas.py auditoria_ik.json
"""
import json
import math
import os
import random
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
for _ruta in (os.path.join(AQUI, '..', 'src', 'arm_broker'), AQUI):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)
try:
    from arm_broker import fk
except ImportError:
    import fk

LIM = fk.JOINT_LIMITS
W_ROT = 150.0      # mm por rad: cuanto pesa el error de orientacion frente al de posicion


# ------------------------------------------------------------------ algebra minima
def _resolver(A, b):
    """Resuelve A x = b (Gauss con pivoteo parcial). A es n x n."""
    n = len(b)
    M = [fila[:] + [b[i]] for i, fila in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        piv = M[c][c]
        if abs(piv) < 1e-12:
            continue
        for r in range(c + 1, n):
            f = M[r][c] / piv
            for k in range(c, n + 1):
                M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / M[r][r] if abs(M[r][r]) > 1e-12 else 0.0
    return x


def _error(T, Tobj, w_rot):
    """Vector de error de 6 componentes: posicion (mm) y orientacion (rad * w_rot)."""
    ep = [Tobj[i][3] - T[i][3] for i in range(3)]
    if w_rot == 0:
        return ep + [0.0, 0.0, 0.0]
    M = [[sum(Tobj[i][k] * T[j][k] for k in range(3)) for j in range(3)] for i in range(3)]
    er = [0.5 * (M[2][1] - M[1][2]), 0.5 * (M[0][2] - M[2][0]), 0.5 * (M[1][0] - M[0][1])]
    return ep + [w_rot * v for v in er]


def _angulo(T, Tobj):
    """Angulo real (rad) entre dos orientaciones. Distingue theta=0 de theta=pi."""
    tr = sum(sum(Tobj[i][k] * T[i][k] for k in range(3)) for i in range(3))
    return math.acos(max(-1.0, min(1.0, (tr - 1.0) / 2.0)))


def _norma(v):
    return math.sqrt(sum(x * x for x in v))


def _recortar(q):
    return [min(max(v, lo), hi) for v, (lo, hi) in zip(q, LIM)]


# ------------------------------------------------------------------ IK numerica
def resolver(Tobj, q_ini, fkm=None, w_rot=W_ROT, iteraciones=70, lam=8.0):
    """Mueve q_ini hasta que fk(q) alcance Tobj. Devuelve (q, error_mm, error_rad)."""
    fkm = fkm or fk.fk_matriz
    q = _recortar(q_ini)
    for _ in range(iteraciones):
        T = fkm(q)
        e = _error(T, Tobj, w_rot)
        if _norma(e[:3]) < 0.02 and (w_rot == 0 or _angulo(T, Tobj) < 2e-4):
            break
        # jacobiano numerico del error
        J = [[0.0] * 6 for _ in range(6)]
        for j in range(6):
            qd = list(q)
            qd[j] += 1e-5
            ed = _error(fkm(qd), Tobj, w_rot)
            for i in range(6):
                J[i][j] = (ed[i] - e[i]) / 1e-5
        JJt = [[sum(J[i][k] * J[m][k] for k in range(6)) + (lam * lam if i == m else 0.0)
                for m in range(6)] for i in range(6)]
        y = _resolver(JJt, e)
        dq = [-sum(J[i][j] * y[i] for i in range(6)) for j in range(6)]
        paso = max(abs(v) for v in dq)
        if paso > 0.5:                       # limita el salto por iteracion
            dq = [v * 0.5 / paso for v in dq]
        q = _recortar([a + b for a, b in zip(q, dq)])
    T = fkm(q)
    e = _error(T, Tobj, w_rot)
    er = _angulo(T, Tobj) if w_rot else 0.0
    return q, _norma(e[:3]), er


def buscar_soluciones(Tobj, semillas=60, rng=1, extra=(), fkm=None, w_rot=W_ROT,
                      tol_pos=0.5, tol_rot=0.01):
    """Todas las configuraciones distintas (dentro de limites) que alcanzan Tobj."""
    az = random.Random(rng)
    ini = [list(q) for q in extra]
    ini += [[az.uniform(lo * 0.95, hi * 0.95) for lo, hi in LIM] for _ in range(semillas)]
    halladas = []
    for s in ini:
        q, ep, er = resolver(Tobj, s, fkm, w_rot)
        if ep > tol_pos or (w_rot and er > tol_rot):
            continue
        if all(max(abs(a - b) for a, b in zip(q, h)) > 0.05 for h in halladas):
            halladas.append(q)
    return halladas


# ------------------------------------------------------------------ descripcion de una rama
def origenes(q):
    """Origen de cada marco DH, con TU tabla (sirve para ver si un eslabon cruza la mesa)."""
    T = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    pts = [(0.0, 0.0, 0.0)]
    for (alpha, a, d, off), th in zip(fk.DH, q):
        T = fk._mul(T, fk._t(alpha, a, d, th + off))
        pts.append((T[0][3], T[1][3], T[2][3]))
    return pts


def describir(q, q_inicial):
    desp = [abs(a - b) for a, b in zip(q, q_inicial)]
    holg = min(min(v - lo, hi - v) for v, (lo, hi) in zip(q, LIM))
    return {
        'q_rad': [round(v, 4) for v in q],
        'q_deg': [round(math.degrees(v), 2) for v in q],
        'signo_q3': '+' if q[2] >= 0 else '-',
        'desp_suma_rad': round(sum(desp), 3),
        'desp_max_rad': round(max(desp), 3),
        'holgura_limites_rad': round(holg, 3),
        'z_min_marcos_mm': round(min(p[2] for p in origenes(q)[1:]), 1),
    }


def analizar_ramas(q_ejec, q_inicial, semillas=60, fkm=None):
    """Compara la solucion del firmware con las otras ramas que alcanzan la misma pose."""
    fkm = fkm or fk.fk_matriz
    Tobj = fkm(q_ejec)
    # semillas dirigidas: el mismo q con el codo (q3) invertido y q2, q4 reajustados
    dirigidas = [[q_ejec[0], q_ejec[1] + d2, -q_ejec[2], q_ejec[3] + d4, q_ejec[4], q_ejec[5]]
                 for d2 in (-0.8, -0.4, 0.0, 0.4, 0.8) for d4 in (-0.8, 0.0, 0.8)]
    sols = buscar_soluciones(Tobj, semillas=semillas, extra=[q_ejec] + dirigidas, fkm=fkm)
    ejec = describir(q_ejec, q_inicial)
    otras = []
    for q in sols:
        if max(abs(a - b) for a, b in zip(q, q_ejec)) < 0.05:
            continue
        d = describir(q, q_inicial)
        d['dist_a_ejecutada_rad'] = round(max(abs(a - b) for a, b in zip(q, q_ejec)), 3)
        otras.append(d)
    contrarias = [d for d in otras if d['signo_q3'] != ejec['signo_q3']]
    return {'ejecutada': ejec, 'otras': otras, 'codo_contrario': contrarias,
            'n_soluciones_distintas': len(otras) + 1}


def hechos_compatibles(res):
    """Frases con DATOS medidos (no la regla del fabricante) que distinguen las ramas."""
    ej, hechos = res['ejecutada'], []
    for alt in res['codo_contrario'][:1]:
        if alt['desp_suma_rad'] > ej['desp_suma_rad']:
            hechos.append(f"la rama contraria exige sumar {alt['desp_suma_rad']:.2f} rad de "
                          f"movimiento articular frente a {ej['desp_suma_rad']:.2f} rad")
        if alt['desp_max_rad'] > ej['desp_max_rad']:
            hechos.append(f"su articulacion que mas se mueve recorre {alt['desp_max_rad']:.2f} rad "
                          f"frente a {ej['desp_max_rad']:.2f} rad")
        if alt['holgura_limites_rad'] < ej['holgura_limites_rad']:
            hechos.append(f"queda a {alt['holgura_limites_rad']:.2f} rad de un limite articular "
                          f"frente a {ej['holgura_limites_rad']:.2f} rad")
        if alt['z_min_marcos_mm'] < 0 <= ej['z_min_marcos_mm']:
            hechos.append(f"un marco del brazo quedaria en z = {alt['z_min_marcos_mm']:.0f} mm "
                          f"(bajo la mesa)")
    return hechos


def imprimir_ramas(res):
    ej = res['ejecutada']
    print(f"  Configuraciones distintas que alcanzan la misma pose: {res['n_soluciones_distintas']}")
    print(f"  solucion del firmware : q3 {ej['signo_q3']}   q(deg)={ej['q_deg']}")
    print(f"      desplazamiento desde la pose inicial: suma={ej['desp_suma_rad']} rad  "
          f"max={ej['desp_max_rad']} rad | holgura a limites={ej['holgura_limites_rad']} rad | "
          f"z min marcos={ej['z_min_marcos_mm']} mm")
    for i, d in enumerate(res['otras'], 1):
        marca = '  <-- CODO CONTRARIO' if d['signo_q3'] != ej['signo_q3'] else ''
        print(f"  alternativa {i}: q3 {d['signo_q3']}   q(deg)={d['q_deg']}{marca}")
        print(f"      suma={d['desp_suma_rad']} rad  max={d['desp_max_rad']} rad | "
              f"holgura={d['holgura_limites_rad']} rad | z min marcos={d['z_min_marcos_mm']} mm")
    if not res['codo_contrario']:
        print('  No encontre una rama con el codo contrario DENTRO de JOINT_LIMITS que alcance la')
        print('  misma pose. Eso no prueba que no exista: es una busqueda numerica con semillas.')
    else:
        h = hechos_compatibles(res)
        print('  Hechos medidos compatibles con la eleccion: ' +
              ('; '.join(h) if h else 'ninguno de los criterios medidos distingue las ramas') + '.')


# ------------------------------------------------------------------ orientacion (rx, ry, rz)
def rpy_a_R(rx, ry, rz):
    """Grados -> matriz 3x3. SUPONE roll-pitch-yaw con R = Rz(rz) * Ry(ry) * Rx(rx).

    Es una suposicion sobre el Euler del firmware: sirve para PREDECIR ramas antes de mover.
    El error medido del reto NO depende de ella (solo usa posicion).
    """
    a, b, c = math.radians(rx), math.radians(ry), math.radians(rz)
    ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    return [[cc * cb, cc * sb * sa - sc * ca, cc * sb * ca + sc * sa],
            [sc * cb, sc * sb * sa + cc * ca, sc * sb * ca - cc * sa],
            [-sb, cb * sa, cb * ca]]


def R_a_rpy(R):
    """Inversa de rpy_a_R (grados)."""
    ry = -math.asin(max(-1.0, min(1.0, R[2][0])))
    if abs(math.cos(ry)) < 1e-9:
        return [math.degrees(math.atan2(-R[1][2], R[1][1])), math.degrees(ry), 0.0]
    return [math.degrees(math.atan2(R[2][1], R[2][2])), math.degrees(ry),
            math.degrees(math.atan2(R[1][0], R[0][0]))]


def pose_T(pos, R):
    return [R[0] + [pos[0]], R[1] + [pos[1]], R[2] + [pos[2]], [0.0, 0.0, 0.0, 1.0]]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1]) as f:
        datos = json.load(f)
    q_ej = [math.radians(v) for v in datos['q_ejecutado_deg']]
    q_ini = [math.radians(v) for v in datos['q_inicial_deg']]
    print(f"Re-analisis de {sys.argv[1]}")
    imprimir_ramas(analizar_ramas(q_ej, q_ini))
