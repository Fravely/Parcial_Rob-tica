#!/usr/bin/env bash
# Terminal C: nodo interprete_ordenes -> servicio /interpretar_orden (Pregunta 1).
# Es el UNICO nodo que habla con el servidor LAYA (HTTP, PC Windows del laboratorio).
#   bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET
#   bash scripts/interprete.sh http://172.51.1.2:8000 multilingual      (valores de practica)
#   bash scripts/interprete.sh                                           (sin URL -> solo respaldo)
# Variables opcionales: TIMEOUT_LAYA (s, defecto 2.0), UMBRAL_LAYA (0..1, defecto 0.60),
#   CONFIANZA_LAYA (0..1, defecto 0.50), OBJETOS (inventario, defecto "cubo";
#   para las 50 frases de la P1 puede ser p. ej. OBJETOS="cubo botella pelota caja")
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
URL="${1:-${LAYA_URL:-}}"
PRESET="${2:-${LAYA_PRESET:-}}"
URL="${URL%/}"
mkdir -p evidencias/pregunta1
LISTA_OBJETOS=""
for o in ${OBJETOS:-cubo}; do LISTA_OBJETOS="${LISTA_OBJETOS:+$LISTA_OBJETOS,}'$o'"; done
echo "Inventario del interprete: [$LISTA_OBJETOS]"
if [[ -n "$URL" ]]; then
    echo "Comprobando LAYA en $URL/health (3 s)..."
    curl -sS --max-time 3 "$URL/health" && echo || \
        echo "AVISO: $URL/health no respondio. El nodo arrancara igual y usara el respaldo si LAYA no contesta."
else
    echo "AVISO: sin URL de LAYA. Todas las decisiones saldran degradadas (fuente=respaldo)."
fi
ARGS=(-r __node:=interprete_ordenes
      --params-file "$PROYECTO/config/interprete_ordenes_logistica.yaml"
      -p timeout_s:="${TIMEOUT_LAYA:-2.0}"
      -p umbral_autorizacion:="${UMBRAL_LAYA:-0.60}"
      -p confianza_minima:="${CONFIANZA_LAYA:-0.50}"
      -p "objetos_disponibles:=[$LISTA_OBJETOS]"
      -p registro_csv:="$PROYECTO/evidencias/pregunta1/interpretaciones.csv")
# Solo se pasan si tienen valor (un -p vacio puede confundir al analizador de argumentos).
if [[ -n "$URL" ]]; then ARGS+=(-p url_laya:="$URL"); fi
if [[ -n "$PRESET" ]]; then ARGS+=(-p modelo_laya:="$PRESET"); fi
exec ros2 run laya_ordenes interprete_ordenes --ros-args "${ARGS[@]}"
