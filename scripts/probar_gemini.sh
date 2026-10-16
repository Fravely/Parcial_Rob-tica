#!/usr/bin/env bash
# Comprueba la clave de Google AI Studio y la conexion a internet SIN mover el robot.
#   bash scripts/probar_gemini.sh                 (prueba de texto)
#   bash scripts/probar_gemini.sh prueba.wav      (ademas transcribe ese audio)
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
if [[ -z "${GEMINI_API_KEY:-}" && -f "$HOME/.clave_gemini" ]]; then
    source "$HOME/.clave_gemini"
fi
exec python3 "$PROYECTO/herramientas/probar_gemini.py" "$@"
