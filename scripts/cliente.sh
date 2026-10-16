#!/usr/bin/env bash
# Terminal de cada integrante (Pregunta 2 con LAYA):
#   texto -> /interpretar_orden (LAYA) -> si permitido -> broker /logistica/pick_place
#   bash scripts/cliente.sh integrante1                          (modo interactivo)
#   bash scripts/cliente.sh integrante1 "recoge el cubo rojo"   (una sola orden)
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
NOMBRE="${1:?Uso: bash scripts/cliente.sh NOMBRE [ORDEN]}"
shift
if [[ "$#" -gt 0 ]]; then
    exec ros2 run laya_ordenes cliente_laya --nombre "$NOMBRE" --accion "$ACCION_BROKER" --orden "$*"
fi
exec ros2 run laya_ordenes cliente_laya --nombre "$NOMBRE" --accion "$ACCION_BROKER"
