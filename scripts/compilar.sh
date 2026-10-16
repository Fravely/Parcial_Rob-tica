#!/usr/bin/env bash
# Compila los CUATRO paquetes: broker + interfaces + LAYA (interprete, clientes y voz).
set -e
PROYECTO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=72
cd "$PROYECTO"
if [[ "${1:-}" == "--limpio" ]]; then
    echo "Borrando build/ install/ log/ de este proyecto (no toca otros workspaces)."
    rm -rf build install log
fi
for marcador in src/laya_ordenes/COLCON_IGNORE src/laya_ordenes_interfaces/COLCON_IGNORE; do
    if [[ -f "$marcador" ]]; then
        echo "Quitando $marcador (venia de logistica_sinLaya1)."
        rm -f "$marcador"
    fi
done
colcon build --symlink-install --packages-select \
    arm_broker_interfaces laya_ordenes_interfaces arm_broker laya_ordenes
source install/local_setup.bash
echo
echo "Ejecutables disponibles:"
ros2 pkg executables arm_broker
ros2 pkg executables laya_ordenes
echo
echo "Compilacion terminada. Abre las terminales indicadas en README.md."
