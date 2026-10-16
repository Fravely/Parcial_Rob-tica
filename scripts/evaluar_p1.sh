#!/usr/bin/env bash
# Pregunta 1: mide las 50 frases contra /interpretar_orden (LAYA) y el clasificador local.
#   bash scripts/evaluar_p1.sh calma [evidencias/pregunta1/50_frases_docente.csv]
#   bash scripts/evaluar_p1.sh carga [evidencias/pregunta1/50_frases_docente.csv]
# OBJETOS debe ser el MISMO inventario con el que se lanzo scripts/interprete.sh.
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
MODO="${1:?Uso: bash scripts/evaluar_p1.sh calma|carga [CSV_50_FRASES]}"
ENTRADA="${2:-$PROYECTO/evidencias/pregunta1/50_frases_docente.csv}"
case "$MODO" in calma|carga) ;; *) echo "El modo debe ser calma o carga" >&2; exit 2 ;; esac
if [[ ! -f "$ENTRADA" ]]; then
    echo "ERROR: no existe $ENTRADA. Copia plantillas: evidencias/pregunta1/plantilla_50_frases_docente.csv" >&2
    exit 1
fi
sed -i 's/\r$//' "$ENTRADA"
SALIDA="$PROYECTO/evidencias/pregunta1/${MODO}.csv"
if [[ -f "$SALIDA" ]]; then
    mv "$SALIDA" "${SALIDA%.csv}_anterior_$(date +%H%M%S).csv"
    echo "Se guardo la corrida anterior con otro nombre."
fi
echo "Calentando la conexion con una frase (no se cuenta)..."
ros2 service call /interpretar_orden laya_ordenes_interfaces/srv/InterpretarOrden \
    "{frase: 'recoge el cubo rojo'}" > /dev/null || true
exec python3 "$PROYECTO/herramientas/evaluar_pregunta1.py" --modo "$MODO" \
    --entrada "$ENTRADA" --salida "$SALIDA" --timeout "${TIMEOUT_CLIENTE:-10}" \
    --objetos ${OBJETOS:-cubo}
