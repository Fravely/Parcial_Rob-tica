#!/usr/bin/env bash
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
exec ros2 topic echo "$TOPICO_COLA"
