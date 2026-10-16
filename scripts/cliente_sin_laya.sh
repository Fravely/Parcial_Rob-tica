#!/usr/bin/env bash
# Respaldo SIN LAYA (reglas locales, fuente LOCAL_SIN_LAYA). Igual que en logistica_sinLaya1.
#   bash scripts/cliente_sin_laya.sh integrante1 ["recoge el cubo rojo"]
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
NOMBRE="${1:?Uso: bash scripts/cliente_sin_laya.sh NOMBRE [ORDEN]}"
shift
if [[ "$#" -gt 0 ]]; then
    exec ros2 run arm_broker cliente_sin_laya --nombre "$NOMBRE" --accion "$ACCION_BROKER" --orden "$*"
fi
exec ros2 run arm_broker cliente_sin_laya --nombre "$NOMBRE" --accion "$ACCION_BROKER"
