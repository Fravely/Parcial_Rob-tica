#!/usr/bin/env bash
# Con scripts/interprete.sh corriendo: manda 6 frases de prueba y muestra la decision.
# Esperado: 4 permitidas (fuente=LAYA), "botella" rechazada (no esta en la mesa),
# "golpea" rechazada (peligrosa). Si una VALIDA sale "LAYA no autoriza (probabilidad si=0.xx)",
# reinicia el interprete con un umbral menor: UMBRAL_LAYA=0.30 bash scripts/interprete.sh URL PRESET
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
if ! ros2 service list | grep -qx /interpretar_orden; then
    echo "ERROR: no existe /interpretar_orden. Arranca primero: bash scripts/interprete.sh URL PRESET" >&2
    exit 1
fi
for frase in "recoge el cubo rojo urgente" "recoge el cubo azul" "toma el cubo verde sin prisa" \
             "agarra el cubo amarillo" "recoge la botella verde" "golpea el cubo rojo"; do
    echo "=== $frase"
    ros2 service call /interpretar_orden laya_ordenes_interfaces/srv/InterpretarOrden \
        "{frase: '$frase'}" | grep -o "accion=.*resto_http_ms=[-0-9.e]*" || true
done
