#!/usr/bin/env bash
# Terminal D (Pregunta 3): voz -> Google AI Studio -> /interpretar_orden -> broker -> brazo.
#   bash scripts/voz.sh                      microfono del Jetson (ENTER graba, ENTER corta)
#   MIC=plughw:2,0 bash scripts/voz.sh       elegir microfono (ver: arecord -l)
#   bash scripts/voz.sh archivo a.wav b.wav  procesar archivos .wav
#   bash scripts/voz.sh texto                demostrar el MODO TEXTO (sin llamar a Google)
#   SEGURO=1 bash scripts/voz.sh             transcribe e interpreta, pero NO envia al broker
#   MODELO_GEMINI=gemini-3.6-flash ...       cambiar el modelo de transcripcion
#   CLAVE_EN_URL=1 ...                       solo si probar_gemini.sh dice que funciono ?key=
# La clave se lee de GEMINI_API_KEY; este script carga ~/.clave_gemini si existe.
set -e
source "$(dirname -- "${BASH_SOURCE[0]}")/entorno.sh"
if [[ -z "${GEMINI_API_KEY:-}" && -f "$HOME/.clave_gemini" ]]; then
    source "$HOME/.clave_gemini"
fi
if [[ -z "${GEMINI_API_KEY:-}${GOOGLE_API_KEY:-}" ]]; then
    echo "AVISO: no hay GEMINI_API_KEY. El nodo funcionara solo en MODO TEXTO." >&2
fi
EVID="$PROYECTO/evidencias/pregunta3"
mkdir -p "$EVID"
ENVIAR=true
if [[ "${SEGURO:-0}" == "1" ]]; then ENVIAR=false; fi
MODO="${1:-microfono}"
ARGS=(-p enviar_al_broker:=$ENVIAR -p client_id:="${CLIENTE_VOZ:-voz}"
      -p accion_broker:="$ACCION_BROKER" -p topico_cola:="$TOPICO_COLA"
      -p timeout_transcripcion_s:="${TIMEOUT_VOZ:-6.0}"
      -p dir_evidencias:="$EVID")
if [[ -n "${MIC:-}" ]]; then ARGS+=(-p dispositivo_alsa:="$MIC"); fi
if [[ -n "${MODELO_GEMINI:-}" ]]; then ARGS+=(-p modelo_gemini:="$MODELO_GEMINI"); fi
if [[ "${CLAVE_EN_URL:-0}" == "1" ]]; then ARGS+=(-p clave_en_url:=true); fi
case "$MODO" in
    microfono) ;;
    texto) ARGS+=(-p forzar_modo_texto:=true) ;;
    archivo)
        shift
        if [[ "$#" -eq 0 ]]; then echo "Uso: bash scripts/voz.sh archivo a.wav [b.wav ...]" >&2; exit 2; fi
        LISTA=""
        for f in "$@"; do
            ABS="$(readlink -f "$f")"
            LISTA="${LISTA:+$LISTA,}'$ABS'"
        done
        ARGS+=(-p fuente_audio:=archivo -p "archivos_audio:=[$LISTA]") ;;
    *) echo "Modo desconocido: $MODO (microfono | texto | archivo)" >&2; exit 2 ;;
esac
exec ros2 run laya_ordenes transcriptor_voz --ros-args "${ARGS[@]}"
