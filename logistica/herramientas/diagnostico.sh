#!/usr/bin/env bash
set -u
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
printf '
=== IP / ROUTE ===
'; hostname -I; ip route get 172.51.1.2 || true
printf '
=== Estado local ROS_DOMAIN_ID ===
%s
' "$ROS_DOMAIN_ID"
printf '
=== paquetes del workspace ===
'; ros2 pkg list | grep -E '^(laya_ordenes|arm_broker)' || true
printf '
=== nodos descubiertos ===
'; ros2 node list || true
printf '
=== endpoints del brazo ===
'; ros2 action list -t || true
printf '
=== editor joint_states ===
'; ros2 topic info /joint_states -v || true
printf '
=== tipos en uso ===
'; ros2 interface show arm_broker_interfaces/action/MoveArm || true
