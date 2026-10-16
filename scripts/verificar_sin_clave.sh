#!/usr/bin/env bash
# Antes de cada git push / entrega: la clave NO puede estar en el repositorio.
# Busca claves nuevas (AQ.xxxx) y antiguas (AIza...). Debe terminar en "OK".
PROYECTO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROYECTO"
if grep -rInE "AQ\.[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,}" . \
        --exclude-dir=build --exclude-dir=install --exclude-dir=log --exclude-dir=.git \
        --exclude-dir=__pycache__ ; then
    echo
    echo "PELIGRO: hay una clave escrita en los archivos de arriba. Borrala antes de entregar." >&2
    exit 1
fi
echo "OK: no hay claves de Google en el proyecto."
