"""Intérprete por reglas locales (modo SIN LAYA). No consulta LAYA ni servicios HTTP.

Se usa con scripts/cliente_sin_laya.sh cuando el servidor LAYA no está disponible.
El camino normal con LAYA es scripts/cliente.sh (laya_ordenes/cliente_laya.py).
"""
import re
import unicodedata

COLORES = ("amarillo", "azul", "verde", "rojo")
FUENTE = "LOCAL_SIN_LAYA"
PRIORIDAD_BAJA, PRIORIDAD_NORMAL, PRIORIDAD_ALTA = 20, 80, 180


def interpretar(frase):
    texto = "".join(c for c in unicodedata.normalize("NFKD", frase.casefold())
                    if not unicodedata.combining(c))
    if re.search(r"\b(golpe\w*|romp\w*|lanz\w*|arroj\w*|forz\w*|aplast\w*|desactiv\w*)\b", texto):
        raise ValueError("Acción no permitida: no se envió al broker.")
    if re.search(r"\b(no|nunca|jamas|evita\w*|cancel\w*|deten\w*)\b", texto):
        raise ValueError("Orden negativa o de cancelación: no se envió ningún movimiento.")
    colores = [c for c in COLORES if re.search(r"\b" + c + r"\b", texto)]
    if len(colores) != 1:
        raise ValueError("Indica un único color: amarillo, azul, verde o rojo.")
    if not re.search(r"\bcubo\b", texto):
        raise ValueError("Esta prueba recoge un cubo por pedido.")
    if not re.search(r"\b(recog\w*|recoj\w*|agarr\w*|tom\w*|levant\w*|coloc\w*|deposit\w*|traslad\w*|llev\w*)\b", texto):
        raise ValueError("Ejemplo de orden: recoge el cubo rojo.")
    # No convertir silenciosamente un destino explícito diferente en 'deposito'.
    destino = re.search(r"\b(?:a|al|hacia|en)\s+(?:(?:la|el|un|una)\s+)?(.+)", texto)
    if destino and not re.match(r"deposito\b", destino.group(1)):
        raise ValueError("El único destino de esta prueba es el depósito.")
    baja = bool(re.search(r"\b(sin prisa|cuando puedas|prioridad baja)\b", texto))
    alta = bool(re.search(r"\b(urgente|inmediatamente|ahora|rapido|prioridad alta)\b", texto))
    if baja and alta:
        raise ValueError("La orden contiene prioridades contradictorias.")
    # Misma escala que el respaldo del interprete (logic.clasificar_respaldo) y que
    # LAYA (score x 50): 20 = sin prisa, 80 = normal, 180 = urgente. Asi un pedido local
    # y uno de LAYA compiten en la misma cola sin que uno aplaste al otro.
    return dict(accion="recoger", objeto="cubo", color=colores[0], zona="deposito",
                priority=PRIORIDAD_BAJA if baja else PRIORIDAD_ALTA if alta else PRIORIDAD_NORMAL,
                permitido=True, degradada=True, fuente=FUENTE)
