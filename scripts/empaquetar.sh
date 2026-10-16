#!/usr/bin/env bash
# Crea ~/logistica_completo.zip sin build/ install/ log/ ni caches (para descargar o respaldar).
set -e
PROYECTO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
bash "$PROYECTO/scripts/verificar_sin_clave.sh"
cd "$(dirname "$PROYECTO")"
NOMBRE="$(basename "$PROYECTO")"
rm -f "$HOME/${NOMBRE}_completo.zip"
zip -r "$HOME/${NOMBRE}_completo.zip" "$NOMBRE" \
    -x "$NOMBRE/build/*" "$NOMBRE/install/*" "$NOMBRE/log/*" "*/__pycache__/*" "*/.ipynb_checkpoints/*"
echo "Listo: $HOME/${NOMBRE}_completo.zip"
