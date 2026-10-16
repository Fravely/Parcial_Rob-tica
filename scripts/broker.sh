#!/usr/bin/env bash
# Terminal B: el broker del RB-2 (UN worker, UNA cola) en modo fisico.
#   bash scripts/broker.sh                 -> politica prioridad, acepta LAYA y respaldo
#   SOLO_LAYA=1 bash scripts/broker.sh     -> rechaza decisiones degradadas (respaldo)
#   POLITICA=fifo bash scripts/broker.sh   -> cola FIFO (comparacion RB-2)
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
EVID="$PROYECTO/evidencias/pregunta2"
mkdir -p "$EVID"
# Un solo broker por Jetson y dominio: tambien bloquea si sigue abierto el de logistica_sinLaya1.
exec 8>/tmp/logistica_sinLaya_broker_72.lock
if ! flock -n 8; then
    echo "ERROR: el broker de logistica_sinLaya1 sigue abierto. Cierralo con Ctrl+C en su terminal." >&2
    exit 1
fi
exec 9>/tmp/logistica_broker_72.lock
if ! flock -n 9; then
    echo "ERROR: ya hay un broker de este proyecto corriendo (otra terminal). Usa ese." >&2
    exit 1
fi
RESPALDO=true
if [[ "${SOLO_LAYA:-0}" == "1" ]]; then RESPALDO=false; fi
echo "Broker: politica=${POLITICA:-prioridad} · respaldo permitido=$RESPALDO · accion=$ACCION_BROKER"
exec ros2 run arm_broker broker --ros-args \
    -r __ns:="$NS_BROKER" \
    -r /arm/queue_state:="$TOPICO_COLA" \
    -r /arm/measured_joint_states:="$TOPICO_MEDIDAS" \
    --params-file "$PROYECTO/config/broker.yaml" \
    -p politica:="${POLITICA:-prioridad}" \
    -p permitir_respaldo_pick_place:=$RESPALDO \
    -p config_item2:="$PROYECTO/config/poses.json" \
    -p evidencias_item2:="$EVID" \
    -p archivo_rechazos:="$EVID/rechazos.csv"
