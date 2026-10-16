# RB-2 — Ítem 3: comparación experimental de políticas de cola

Esta reconstrucción sigue `TUTORIAL_ITEM2.md`, `probar_politicas.py`, `generar_carga.py`,
`cliente.py` y `verificar_exclusion.py` facilitados por el compañero. **No contamos con
la consigna íntegra original del ítem 3 de RB-2**; antes de entregar coteja con la rúbrica.

## Diseño (escribir predicciones ANTES de medir)

- Configuración: 4 clientes (`ana:1`, `luis:3`, `eva:5`, `tom:7`). `uint8 priority`
  en **ESTA** versión: MAYOR número = más urgente.
- Política 1 `fifo`: menor `t_llegada` primero.
- Política 2 `prioridad`: `prioridad + espera_s / tau`, tau = 8.0 s,
  empate a favor de quien llegó antes. Evita inanición bajo las hipótesis del tutorial.
- 15 destinos por cliente (60 goals totales), **mismas poses, mismo orden** en ambos ensayos,
  `duracion_movimiento_s=3.0`, `paso_max_rad=2.0`, `cola_max=20`, una petición activa
  por cliente (el siguiente goal se envía cuando concluye el anterior).
- Estima **antes** p95 de espera de cada política, tasa de aceptación y razón de la diferencia.
  Usa `plantillas/predicciones_rb2_item3.csv` y firma o pon marca de tiempo antes de la corrida.
- Hipótesis previa orientativa del tutorial: al envejecer, prioridades bajas
  dejan de perder turno ante llegadas urgentes continuas. NO sustituye resultados observados.

## 0. Pruebas sin hardware

Desde `~/logistica`, con Python:

```bash
python3 herramientas/probar_politicas.py
python3 herramientas/probar_broker_sin_ros.py
python3 herramientas/generar_carga.py --n 15 --semilla 7 --salida plantillas/carga_rb2.csv
```

Son **simulaciones**, no bags físicos. Revisa que las 15 poses caben dentro de límites.

## 1. Preparación para ROS, SIN MOVIMIENTO REAL

Una terminal nueva que no cargue `~/rb2_ws/install` ni `~/jetcobot_ws/install`:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
cd ~/logistica
source install/setup.bash
ros2 action list -t
ros2 interface show arm_broker_interfaces/action/MoveArm
```

Debe mostrar `joint_positions` (NO `q_deseado`). **Detén otros brokers** antes de continuar.

**Terminal A - broker simulado, cola FIFO**:

```bash
cd ~/logistica
ros2 run arm_broker broker --ros-args   -p politica:=fifo -p paso_max_rad:=2.0   -p publicar_joint_states:=false -p archivo_rechazos:="$(pwd)/evidencias/rechazos_fifo.csv"
```

Para comparar con prioridad detén A con `Ctrl+C` y reinicia:

```bash
ros2 run arm_broker broker --ros-args   -p politica:=prioridad -p tau_envejecimiento_s:=8.0   -p paso_max_rad:=2.0 -p publicar_joint_states:=false   -p archivo_rechazos:="$(pwd)/evidencias/rechazos_prioridad.csv"
```

Por defecto el broker NO envía mensajes a `/joint_states` aunque un goal termine
con `success=true` (en el resultado el mensaje dirá **SIMULADO**). NO afirmar que
el brazo se movió. Verificar estado de cola y feedback, NO exclusión física.

## 2. Cuatro clientes concurrentes y CSV

En otra terminal de JetCobot, sin otros brokers:

```bash
cd ~/logistica
source /opt/ros/humble/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=52
CONFIRMAR_CLIENTES=SI bash herramientas/lanzar_cuatro_clientes.sh fifo
```

El script usa clientes `ana`, `luis`, `eva`, `tom`, cada uno con 15 pedidos.
Al cambiar broker a `prioridad`, sustituye `fifo` por `prioridad`.
No uses este script contra el broker de `~/rb2_ws`: su tipo de acción es diferente.

### Si se requieren medidas físicas reales

**Solo después** de supervisión, calibración, confirmar `joint_states` con **un
solo publicador**, driver correcto, límites, zona libre, base q_inicial real,
y autorización del docente; iniciar broker con `-p publicar_joint_states:=true`.
Esto hará que el robot pueda moverse; no es adecuado para ensayar conectividad.
Además, estos scripts NO operan gripper o MoveIt2. Las pruebas físicas del RB-2
se deben registrar con un `ros2 bag` y vídeos. No ejecutes en paralelo otro controlador.

## 3. Bag real del broker (una terminal por corrida)

Con broker correcto, y cuando corresponda, registra ANTES de mandar clientes:

```bash
mkdir -p evidencias/fifo
ros2 bag record -s sqlite3 -o evidencias/fifo_bag /arm/queue_state /joint_states
```

Control-C al terminar los cuatro clientes. Otra corrida con `prioridad`:

```bash
ros2 bag record -s sqlite3 -o evidencias/prioridad_bag /arm/queue_state /joint_states
```

Los nombres `fifo_bag` y `prioridad_bag` deben ser nuevos (rosbag rechaza la carpeta si ya existe).
Un bag con broker `publicar_joint_states=false` NO tendrá movimientos de joint_states;
la verificación de exclusión requiere publicaciones reales.

## 4. Procesar los bags y medir

```bash
python3 herramientas/exportar_csv.py evidencias/fifo_bag --salida evidencias/fifo_bag_csv
python3 herramientas/exportar_csv.py evidencias/prioridad_bag --salida evidencias/prioridad_bag_csv
python3 herramientas/verificar_exclusion.py evidencias/fifo_bag_csv/queue_state.csv evidencias/fifo_bag_csv/joint_states.csv
python3 herramientas/verificar_exclusion.py evidencias/prioridad_bag_csv/queue_state.csv evidencias/prioridad_bag_csv/joint_states.csv
python3 herramientas/metricas_item3.py --fifo 'evidencias/fifo/*.csv' --prioridad 'evidencias/prioridad/*.csv'
```

Métricas: por cliente/total mediana de espera, percentil 95 lineal,
max, tasa de goals completados por segundo durante el intervalo observable,
y equidad de Jain de `1/(1+espera media)` por cliente.
**Esa definición de Jain es una elección de análisis, no está especificada en
los materiales disponibles**. Evita calcular Jain de la cantidad final de goals
por cliente si cada cliente manda obligatoriamente el mismo número: da 1.0 trivial.

La verificación de exclusión mediante muestreo (5 Hz) es una evidencia parcial;
también debes mostrar `ros2 topic info /joint_states -v` y `Publisher count: 1`.

## Evidencias para entregar

- Predicciones previas al ensayo (CSV firmado), dos bags y sus CSV
- Logs de clientes y broker; capturas `Publisher count: 1`, cero intercalaciones
- Mediana, p95, max, throughput, métrica de equidad, tasa de rechazos
- Comparación explicada con números medidos, nunca resultados inventados
