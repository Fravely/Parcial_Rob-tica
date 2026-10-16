#!/usr/bin/env bash
# RB2 item 3: cuatro clientes simultaneos contra el broker de ~/logistica.
# SEGURIDAD: aborta si el broker permite publicar /joint_states.
set -Eeuo pipefail

POLITICA="${1:-}"
if [[ "${CONFIRMAR_CLIENTES:-}" != 'SI' || ( "$POLITICA" != 'fifo' && "$POLITICA" != 'prioridad' ) ]]; then
  echo 'Uso: CONFIRMAR_CLIENTES=SI bash herramientas/lanzar_cuatro_clientes.sh fifo|prioridad' >&2
  exit 2
fi

PROYECTO="$HOME/logistica"
cd "$PROYECTO"
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=72   # dominio del equipo (JetCobot 172.51.1.18)
source "$PROYECTO/install/local_setup.bash"

if [[ ! -s "$PROYECTO/plantillas/carga_rb2.csv" ]]; then
  echo 'ERROR: falta plantillas/carga_rb2.csv o esta vacio.' >&2
  exit 2
fi

PREFIJO="$(ros2 pkg prefix arm_broker)" || exit 2
case "$PREFIJO" in
  "$PROYECTO/install"|"$PROYECTO/install/"*) ;;
  *) echo "ERROR: se esta usando arm_broker de otro workspace: $PREFIJO" >&2; exit 2 ;;
esac

if ! ros2 pkg executables arm_broker | grep -qx 'arm_broker cliente'; then
  echo 'ERROR: no aparece el ejecutable arm_broker cliente del proyecto logistica.' >&2
  echo 'Revisa: ros2 pkg executables arm_broker; recompila logistica y abre terminal limpia.' >&2
  exit 2
fi

if ! ros2 action list -t | grep -Fqx '/move_arm [arm_broker_interfaces/action/MoveArm]'; then
  echo 'ERROR: /move_arm no esta disponible con la interfaz esperada.' >&2
  exit 2
fi

PUBLICA="$(ros2 param get /arm_broker publicar_joint_states)" || exit 2
if ! grep -qx 'Boolean value is: False' <<< "$PUBLICA"; then
  echo "SEGURIDAD: broker NO confirmado como simulado: $PUBLICA" >&2
  echo 'No se enviaron objetivos.' >&2
  exit 2
fi

POLITICA_ACTUAL="$(ros2 param get /arm_broker politica)" || exit 2
if [[ "$POLITICA_ACTUAL" != "String value is: $POLITICA" ]]; then
  echo "ERROR: broker usa '$POLITICA_ACTUAL', pero pediste '$POLITICA'." >&2
  echo 'Reinicia el broker con la politica correcta.' >&2
  exit 2
fi

SALIDA="$PROYECTO/evidencias/$POLITICA"
mkdir -p "$SALIDA"
for nombre in ana luis eva tom; do
  if [[ -e "$SALIDA/$nombre.csv" ]]; then
    echo "ERROR: ya existe $SALIDA/$nombre.csv. Respalda/renombra la corrida antes de repetir." >&2
    exit 2
  fi
done

pids=()
limpiar() {
  for pid in "${pids[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
}
trap limpiar INT TERM

for entrada in 'ana 1' 'luis 3' 'eva 5' 'tom 7'; do
  read -r CLIENTE PRIORIDAD <<< "$entrada"
  echo "Iniciando $CLIENTE con prioridad $PRIORIDAD ($POLITICA; SOLO SIMULACION)"
  ros2 run arm_broker cliente --ros-args \
    -p client_id:="$CLIENTE" \
    -p priority:="$PRIORIDAD" \
    -p traza:="$PROYECTO/plantillas/carga_rb2.csv" \
    -p repeticiones:=1 -p pausa_s:=0.5 \
    -p resultados_csv:="$SALIDA/$CLIENTE.csv" \
    > "$SALIDA/$CLIENTE.log" 2>&1 &
  pids+=("$!")
done

fallos=0
for i in "${!pids[@]}"; do
  if ! wait "${pids[$i]}"; then
    echo "ERROR: cliente PID ${pids[$i]} termino con fallo. Revisa $SALIDA/*.log" >&2
    fallos=$((fallos+1))
  fi
done
trap - INT TERM

printf '\nResultados de %s:\n' "$POLITICA"
for nombre in ana luis eva tom; do
  if [[ -f "$SALIDA/$nombre.csv" ]]; then
    printf '  %-8s %s filas de datos\n' "$nombre" "$(( $(wc -l < "$SALIDA/$nombre.csv") - 1 ))"
  else
    printf '  %-8s NO GENERO CSV\n' "$nombre"
    fallos=$((fallos+1))
  fi
done
if (( fallos )); then
  echo "ATENCION: $fallos errores. Revisar archivos .log antes de continuar." >&2
  exit 1
fi
echo 'Cuatro clientes completaron la corrida simulada. NO es evidencia de movimiento fisico.'
