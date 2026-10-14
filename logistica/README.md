# LOGISTICA — JetCobot ROS 2 Humble — Proyecto nuevo desde cero

**IP Jetson vista en clase: 172.51.9.15; ROS_DOMAIN_ID=52.**

## Contenido

- `src/arm_broker_interfaces`: `MoveArm.action` y `QueueState.msg` compatibles con
  el **`broker.py` recibido inicialmente**, no con el distinto `~/rb2_ws` del Jetson.
- `src/arm_broker`: worker único, FIFO, prioridad con envejecimiento, FK y cliente CSV.
- `src/laya_ordenes_interfaces`: servicio tipado `/interpretar_orden`.
- `src/laya_ordenes`: consultas HTTP a LAYA, timeout y respaldo, puente seguro a broker.
- `herramientas/`: pruebas sin ROS, generación de carga, bags -> CSV, métricas RB2 ítem 3,
  verificador de exclusión y evaluador de 50 frases.
- `referencia_codigos_companero/`: copias **sin modificar** de códigos recibidos.
- `docs/COMANDOS_QUE_FUNCIONARON_Y_ERRORES.md`: historial de comandos de la sesión y solución.
- `docs/RB2_ITEM3.md`: protocolo experimental y métricas.
- `docs/CONTRATOS_Y_LIMITACIONES.md`: compatibilidades y lo pendiente.

**AVISO:** el `kinematics.py` cuestionado NO forma parte del proyecto. Este proyecto
usa `fk.py` recibido. No hay conexión LAYA real demostrada ni agarre completo.

## 1. Instalación limpia (en Jetson mediante JupyterLab)

1. Descarga el ZIP a tu computadora, súbelo desde JupyterLab en `172.51.9.15:8888` a `/home/jetson`.
2. Asegúrate de que la carpeta `~/logistica` NO exista ya o cambia el nombre del proyecto antiguo.
3. Descomprime **fuera de los workspaces existentes**:

```bash
cd ~
unzip -q logistica_completa_jetcobot.zip
cd ~/logistica
ls src
```

**Detén primero con Ctrl+C el intérprete y el broker de proyectos antiguos**; no
pueden ofrecer simultáneamente los mismos servicios/acciones en `ROS_DOMAIN_ID=52`.
No uses `source ~/rb2_ws/install/setup.bash` ni `source ~/jetcobot_ws/install/setup.bash`
para ejecutar este proyecto. Abre una terminal NUEVA:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
cd ~/logistica
colcon list --names-only
colcon build --symlink-install
source install/setup.bash
ros2 pkg list | grep -E '^(laya_ordenes|arm_broker)'
ros2 interface show arm_broker_interfaces/action/MoveArm
ros2 interface show laya_ordenes_interfaces/srv/InterpretarOrden
```

La interfaz debe contener `joint_positions`. Si dice `q_deseado`, tienes
cargada la otra versión: vuelve a terminal nueva y revisa los overlays.

## 2. Probar todo SIN MOVER el robot

```bash
cd ~/logistica
python3 -m unittest discover -s tests -v
python3 herramientas/probar_politicas.py
python3 herramientas/probar_broker_sin_ros.py
```

Inicia **Terminal A**:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
cd ~/logistica
source install/setup.bash
ros2 run laya_ordenes interprete_ordenes --ros-args   -p url_laya:='' -p timeout_s:=2.0   -p objetos_disponibles:="['cubo','botella','pelota','caja']"   -p registro_csv:="$(pwd)/evidencias/interpretaciones.csv"
```

El valor por defecto de `url_laya` es vacío y fuerza el **respaldo**. El servidor Windows del profesor NO se verificó.

**Terminal B** (también source /opt + source ~/logistica/install + export dominio):

```bash
ros2 service list | grep interpretar
ros2 service call /interpretar_orden   laya_ordenes_interfaces/srv/InterpretarOrden   "{frase: 'recoge el cubo rojo urgente'}"
```

Debes ver `objeto=cubo, color=rojo, degradada=True, fuente=respaldo`.

**Terminal C - broker SOLO EN MODO SIMULADO, NO PUBLICA MOVIMIENTO:**

```bash
cd ~/logistica
ros2 run arm_broker broker --ros-args   -p politica:=prioridad -p tau_envejecimiento_s:=8.0   -p publicar_joint_states:=false
```

**Terminal B - puente sin goal (modo seguro)**

```bash
ros2 run laya_ordenes orden_a_broker --ros-args   -p frase:='recoge el cubo rojo urgente' -p habilitar_movimiento:=false
```

¡No pone el gripper, no hace IK del objeto, no hace agarre! Si falla, revisar `ros2 service list`, tipos y el CSV.

## 3. Usar LAYA real CUANDO EL DOCENTE ENTREGUE LA DIRECCIÓN

El servidor corre en Windows del laboratorio, NO hay que instalar/trenar LAYA en Jetson.
Obtener IP, puerto y preset **reales** antes de cambiar `url_laya`:

```bash
curl -v --connect-timeout 5 http://IP_DOCENTE:PUERTO/v1/systemone
# GET puede devolver 405; confirma red/proceso, no que el modelo infiera.
```

Ejecutar A con `-p url_laya:=http://IP_DOCENTE:PUERTO` y `-p modelo_laya:=PRESET_DOCENTE`
**solo si el docente confirma el valor del modelo**. El nodo envía `POST /v1/systemone`.
El campo `degradada=False`, `fuente=LAYA` significa que obtuvo respuesta tipada real.
`LAYA_API_KEY` es variable de entorno si ese servidor necesita autenticación.

## 4. Ítem 3 del Reto 2: resultados medibles

Lee primero **`docs/RB2_ITEM3.md`**. Hay scripts para generar la misma carga,
cuatro clientes, CSV, bag sqlite3, latencia p95, fairness y exclusión mutua.
**No asumas** que la simulación reemplaza las evidencias de brazo real.

## 5. Lo que todavía falta

- confirmar IP/puerto/preset Windows LAYA;
- reemplazar inventario ejemplo por cuatro objetos físicos; obtener frases del docente;
- localización cámara/IK/MoveIt2/gripper y validaciones reales para el examen;
- transcripción por Google AI Studio (no forma parte aún de este ZIP).

**Nunca mezclar** la versión de `~/rb2_ws` con este `MoveArm.action`.
Lee `docs/COMANDOS_QUE_FUNCIONARON_Y_ERRORES.md` para fallos específicos reales.
