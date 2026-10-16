#!/usr/bin/env bash
# Se carga con "source" desde los demas scripts. Tambien se puede usar a mano:
#   source scripts/entorno.sh
PROYECTO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export PROYECTO
source /opt/ros/humble/setup.bash
# Dominio asignado al equipo (JetCobot 172.51.1.18). Un equipo que mueva otro brazo pierde la pregunta.
export ROS_DOMAIN_ID=72
# Espacio de nombres del broker de este proyecto: accion, cola y lecturas del brazo.
export NS_BROKER=/logistica
export ACCION_BROKER="$NS_BROKER/pick_place"
export TOPICO_COLA="$NS_BROKER/arm/queue_state"
export TOPICO_MEDIDAS="$NS_BROKER/arm/measured_joint_states"
if [[ -f "$PROYECTO/install/local_setup.bash" ]]; then
    source "$PROYECTO/install/local_setup.bash"
else
    echo "AVISO: aun no hay install/. Ejecuta primero: bash scripts/compilar.sh" >&2
fi
cd "$PROYECTO"
