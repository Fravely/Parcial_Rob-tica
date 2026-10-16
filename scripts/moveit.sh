#!/usr/bin/env bash
# Terminal A: MoveIt2 SOLO como planificador (FK, IK y trayectoria). Nunca ejecuta:
# la ejecucion fisica la hace el worker del broker por pymycobot.
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
CONFIG_MOVEIT_LOCAL="$PROYECTO/config/moveit_local.yaml"
# Reutiliza la configuracion ya generada y probada en logistica_sinLaya1, si existe.
if [[ ! -f "$CONFIG_MOVEIT_LOCAL" ]]; then
    for previo in "$HOME/logistica_sinLaya1/config/moveit_sin_laya.yaml" \
                  "$HOME/logistica_sinLaya/config/moveit_sin_laya.yaml"; do
        if [[ -f "$previo" ]]; then
            cp "$previo" "$CONFIG_MOVEIT_LOCAL"
            echo "Se copio la configuracion de MoveIt ya probada: $previo"
            break
        fi
    done
fi
if [[ -f "$CONFIG_MOVEIT_LOCAL" ]]; then
    echo "MoveIt con $CONFIG_MOVEIT_LOCAL (estado del brazo <- $TOPICO_MEDIDAS)"
    exec ros2 run moveit_ros_move_group move_group --ros-args \
        --params-file "$CONFIG_MOVEIT_LOCAL" \
        -r /joint_states:="$TOPICO_MEDIDAS"
fi
echo "Primera preparacion: deja este MoveIt abierto y ejecuta en otra terminal:"
echo "    cd $PROYECTO && source scripts/entorno.sh && python3 reparar_moveit.py"
echo "Cuando diga CONFIGURACION LOCAL LISTA, Ctrl+C aqui y vuelve a ejecutar bash scripts/moveit.sh"
exec ros2 launch jetcobot_moveit move_group.launch.py allow_trajectory_execution:=false
