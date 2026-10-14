"""Políticas de cola — ítems 2 y 3."""

import threading
import time


class Pedido:
    def __init__(self, goal_handle, client_id, priority, joint_positions):
        self.goal_handle = goal_handle
        self.goal_id = bytes(goal_handle.goal_id.uuid).hex()[:12]
        self.client_id = client_id
        self.priority = int(priority)
        self.joint_positions = list(joint_positions)
        self.t_llegada = time.time()
        self.t_inicio_ejec = None
        self.fin = threading.Event()
        self.resultado = None

    @property
    def espera_s(self):
        fin = self.t_inicio_ejec if self.t_inicio_ejec else time.time()
        return fin - self.t_llegada

    def __repr__(self):
        return f'<{self.client_id} p{self.priority} {self.goal_id}>'


class Politica:
    nombre = 'base'

    def siguiente(self, pendientes):
        raise NotImplementedError

    def atendido(self, pedido):
        pass


# ============================== IMPLEMENTAR · ítems 2 y 3 =========================
class FIFO(Politica):
    """Atiende en orden de llegada."""
    nombre = 'fifo'

    def siguiente(self, pendientes):
        if not pendientes:
            return None
        return min(range(len(pendientes)), key=lambda i: pendientes[i].t_llegada)


class SegundaPolitica(Politica):
    """Prioridad con envejecimiento.

    puntaje = prioridad + espera_s / tau   (mayor puntaje = se atiende antes)
    Cada tau segundos de espera equivalen a subir un nivel de prioridad, así que
    la espera de un pedido de prioridad p queda acotada a ~ (p_max - p) * tau
    más lo que dure el movimiento en curso. Empate: gana el que llegó antes.
    """
    nombre = 'prioridad'

    def __init__(self, tau_envejecimiento_s=8.0):
        self.tau = max(1e-3, float(tau_envejecimiento_s))

    def puntaje(self, pedido):
        return pedido.priority + pedido.espera_s / self.tau

    def siguiente(self, pendientes):
        if not pendientes:
            return None
        return max(range(len(pendientes)),
                   key=lambda i: (self.puntaje(pendientes[i]), -pendientes[i].t_llegada))
# =================================================================================


POLITICAS = {
    'fifo': FIFO,
    'prioridad': SegundaPolitica,
}
