#!/usr/bin/env bash
# Evidencia ros2 bag. Iniciar ANTES de enviar ordenes; Ctrl+C al terminar.
#   bash scripts/grabar.sh p2     (Pregunta 2)     bash scripts/grabar.sh p3     (Pregunta 3)
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
PREG="${1:-p2}"
case "$PREG" in
    p2) DIR="$PROYECTO/evidencias/pregunta2" ;;
    p3) DIR="$PROYECTO/evidencias/pregunta3" ;;
    *) echo "Uso: bash scripts/grabar.sh p2|p3" >&2; exit 2 ;;
esac
mkdir -p "$DIR"
exec ros2 bag record --include-hidden-topics -o "$DIR/bag_${PREG}_$(date +%Y%m%d_%H%M%S)" \
    "$TOPICO_COLA" "$TOPICO_MEDIDAS" \
    "$ACCION_BROKER/_action/feedback" "$ACCION_BROKER/_action/status" \
    /voz/transcripcion /voz/estado /interfaz/ordenes /rosout
