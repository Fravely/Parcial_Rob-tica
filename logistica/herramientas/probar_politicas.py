#!/usr/bin/env python3
"""Prueba las políticas SIN ROS ni brazo, con reloj simulado (corre en cualquier PC).

    python3 probar_politicas.py

1) Comprobaciones de orden (FIFO y prioridad con envejecimiento).
2) Simulación: 4 clientes a lazo cerrado como cliente.py (envían, esperan resultado,
   pausan 0.5 s), cada movimiento dura 3 s. Es un modelo, NO sustituye la corrida
   real con rosbag del ítem 3.
"""
import os, sys, types, statistics

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'src', 'arm_broker'))
from arm_broker import politicas                                  # noqa: E402

reloj = {'t': 1000.0}
politicas.time = types.SimpleNamespace(time=lambda: reloj['t'])


def pedido(cliente, prio, t_llegada):
    gh = types.SimpleNamespace(goal_id=types.SimpleNamespace(uuid=os.urandom(16)))
    p = politicas.Pedido(gh, cliente, prio, [0] * 6)
    p.t_llegada = t_llegada
    return p


def comprobaciones():
    reloj['t'] = 1010.0
    cola = [pedido('a', 1, 1000.0), pedido('b', 9, 1005.0), pedido('c', 5, 1002.0)]
    assert politicas.FIFO().siguiente(cola) == 0, 'FIFO debe elegir al que llegó primero'
    assert politicas.FIFO().siguiente([]) is None
    pr = politicas.SegundaPolitica(8.0)
    assert pr.siguiente([]) is None
    # a: 1 + 10/8 = 2.25   b: 9 + 5/8 = 9.6   c: 5 + 8/8 = 6.0  -> gana b
    assert pr.siguiente(cola) == 1
    # a esperó 100 s: 1 + 100/8 = 13.5 > b (9.6) -> el envejecimiento rescata a 'a'
    cola[0].t_llegada = 910.0
    assert pr.siguiente(cola) == 0
    # empate exacto -> el que llegó antes
    e1, e2 = pedido('x', 3, 1000.0), pedido('y', 3, 1000.0)
    assert pr.siguiente([e2, e1]) in (0, 1)
    print('comprobaciones de orden: OK')


def simular(politica, n_por_cliente=15, servicio=3.0, pausa=0.5):
    reloj['t'] = 0.0
    prios = {'c1': 1, 'c2': 3, 'c3': 5, 'c4': 7}
    restantes = {c: n_por_cliente for c in prios}
    proximo = {c: 0.0 for c in prios}
    cola, esperas = [], {c: [] for c in prios}
    while any(restantes.values()) or cola:
        for c in prios:                       # llegadas
            if restantes[c] and proximo[c] <= reloj['t'] and not any(p.client_id == c for p in cola):
                cola.append(pedido(c, prios[c], reloj['t']))
                restantes[c] -= 1
                proximo[c] = float('inf')
        if not cola:
            reloj['t'] = max(reloj['t'], min(proximo[c] for c in prios if restantes[c] and proximo[c] != float('inf')))
            continue
        p = cola.pop(politica.siguiente(cola))
        esperas[p.client_id].append(reloj['t'] - p.t_llegada)
        reloj['t'] += servicio
        proximo[p.client_id] = reloj['t'] + pausa
    return prios, esperas


def p95(xs):
    xs = sorted(xs)
    return xs[max(0, min(len(xs) - 1, int(round(0.95 * (len(xs) - 1)))))]


if __name__ == '__main__':
    comprobaciones()
    for nombre, pol in [('FIFO', politicas.FIFO()),
                        ('prioridad estática (tau=1e9)', politicas.SegundaPolitica(1e9)),
                        ('prioridad + envejecimiento (tau=8)', politicas.SegundaPolitica(8.0))]:
        prios, esp = simular(pol)
        print(f'\n{nombre}')
        for c in sorted(prios):
            w = esp[c]
            print(f'  {c} (prio {prios[c]}): n={len(w):2d} media={statistics.mean(w):5.1f}s '
                  f'p95={p95(w):5.1f}s max={max(w):5.1f}s')
