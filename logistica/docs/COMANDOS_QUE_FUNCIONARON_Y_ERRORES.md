# Comandos probados en TUS capturas del JetCobot y solución de errores

**Equipo observado:** JetCobot `172.51.9.15`, ROS 2 Humble,
`ROS_DOMAIN_ID=52`. Windows consultado: `172.51.1.2`.
No confundir **comando que se ejecutó** con **resultado de LAYA correcto**.

## 1. Funcionaron y su resultado se vio en capturas

**Terminal Jetson (JupyterLab)**

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
cd ~/jetcobot_ws
ls src | grep -E 'arm_broker|laya'   # vacío ANTES de instalar
ping -c 4 172.51.1.2            # recibió 4/4 respuestas
ip route get 172.51.1.2         # via wlp1p1s0, src 172.51.9.15
```

**Compilar el kit LAYA antiguo después de solucionar duplicados (SE HIZO)**

```bash
cd ~/jetcobot_ws
touch kit_laya_jetcobot/COLCON_IGNORE
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
colcon build --symlink-install --packages-select laya_ordenes_interfaces laya_ordenes
source ~/jetcobot_ws/install/setup.bash
ros2 pkg list | grep laya
```

Captura: `Summary: 2 packages finished`, luego `laya_ordenes` y
`laya_ordenes_interfaces`. **No repetir en el proyecto nuevo**; esos fueron los comandos del proyecto anterior.

**Servicio `/interpretar_orden` (SE HIZO)**

```bash
ros2 service list | grep interpretar
ros2 service call /interpretar_orden   laya_ordenes_interfaces/srv/InterpretarOrden   "{frase: 'recoge el cubo rojo urgente'}"
```

La prueba confirmó la acción `recoger`, objeto `cubo`, color `rojo`,
prioridad `180`, `permitido=true`, `degradada=true`, `fuente=respaldo`.
La ejecución que lo consiguió incluyó el parámetro:

```bash
ros2 run laya_ordenes interprete_ordenes --ros-args   -p url_laya:=http://172.51.1.2:8800 -p timeout_s:=2.0   -p objetos_disponibles:="['cubo','botella','pelota','caja']"
```

**IMPORTANTE: LAYA real NO respondió**; la prueba solo verificó el respaldo.

**Búsqueda y compilación del broker existente distinto (SE HIZO)**

```bash
find ~/jetcobot_ws ~/rb2_ws -name broker.py 2>/dev/null
find ~/jetcobot_ws ~/rb2_ws -name setup.py 2>/dev/null | grep arm_broker
ros2 interface show arm_broker_interfaces/action/MoveArm
ls -R ~/rb2_ws/src/arm_broker | head -70
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
cd ~/rb2_ws
colcon list --names-only
colcon build --symlink-install --packages-select arm_broker
source ~/rb2_ws/install/setup.bash
ros2 pkg list | grep arm_broker
ros2 pkg executables arm_broker
```

Captura: `Summary: 1 package finished`, ejecutable `arm_broker_node`.
**NO mezclar el broker `rb2_ws` con el nuevo `logistica`:** en `rb2_ws`
`MoveArm.action` usa `q_deseado`, mayor urgencia con valores MENORES;
en el código `broker.py` inicialmente entregado usa `joint_positions`
y mayor urgencia con números MAYORES.

**PowerShell en Windows (SE HIZO)**

```powershell
ipconfig
Test-NetConnection 172.51.9.15 -InformationLevel Detailed
Get-NetTCPConnection -LocalPort 8000 -State Listen
Get-NetTCPConnection -LocalPort 8800 -State Listen
Get-NetTCPConnection -State Listen | Select LocalAddress,LocalPort,OwningProcess | Sort LocalPort
Get-CimInstance Win32_Process | Where-Object {
 $_.Name -match 'python|laya|uvicorn|docker' -or
 $_.CommandLine -match 'laya|uvicorn|systemone'
} | Select-Object ProcessId,Name,CommandLine | Format-List
```

`Test-NetTCPConnection ...` NO es un comando Bash. Windows alcanzó el Jetson.
No hubo listeners en 8000 ni 8800; no se encontraron procesos LAYA con ese filtro.
Eso **no prueba que no esté instalado en otra máquina**.

## 2. Errores que aparecieron y cómo resolverlos

| Error real | Causa observada | Solución comprobada o acción correcta |
| --- | --- | --- |
| `colcon ERROR: Duplicate package names` | kit LAYA antiguo dentro del workspace más copia en src/ | `touch kit_laya_jetcobot/COLCON_IGNORE` (FUNCIONÓ). En `~/logistica` evitar copias extra bajo el workspace. |
| `ros2 service list` sin intérprete | Nodo no iniciado o entorno equivocado | `source /opt/ros/humble/setup.bash; source ~/logistica/install/setup.bash; export ROS_DOMAIN_ID=52`; inicia un SOLO intérprete. |
| `objeto='ninguno'`, `permitido=False` | Inventario vacío | `-p objetos_disponibles:="['cubo','botella','pelota','caja']"` (FUNCIONÓ). Reemplazar con inventario real. |
| `TimeoutError: LAYA superó timeout_s=2.00` | Servidor inaccesible a IP/puerto consultados | Solicitar IP, puerto y preset docente; probar desde Windows y Jetson. Respaldo funcionó, no es inferencia LAYA. |
| `curl: (28) Connection timed out` a `172.51.1.2:8800` | Sin servicio accesible en ese puerto | `ping -c 4 172.51.1.2` verificó red. Revisar puerto real, proceso/Firewall/Windows correctos. No adivinar otro puerto. |
| PowerShell `Get-NetTCPConnection` en Bash: `command not found` | Comando Windows ejecutado en Linux | Usar PowerShell Windows. |
| `curl: (3) URL using bad/illegal format` | Multilínea con `\` o salto errado | Una sola línea: `curl -v --connect-timeout 5 http://IP:PUERTO/v1/systemone` (un GET puede ser 405). |
| `Package 'arm_broker' not found` en antiguo `rb2_ws` | Solo interfaces instaladas en ese momento | `colcon build --symlink-install --packages-select arm_broker` dentro de `~/rb2_ws`; FUNCIONÓ. |
| `Unknown topic '/joint_states'` | No había endpoints descubiertos | No implica falla hardware. Arrancar el nodo/controlador correcto bajo supervisión y ejecutar `ros2 topic info /joint_states -v`. |
| `ros2 action list -t` vacío | No se encontró broker ejecutándose | Verifica el ejecutable y que haya solo un broker por dominio. |
| `AttributeError: q_deseado` o `joint_positions` | Se mezclaron dos versiones incompatibles de MoveArm.action | No combinar `rb2_ws` con `logistica` en el mismo entorno/DDS. Mostrar `ros2 interface show` y detener broker equivocado. |

## 3. Nuevos comandos que todavía NO se han probado en el robot

Los comandos para la carpeta nueva `~/logistica` se encuentran en `README.md`.
Se pueden ejecutar en el Jetson tras comprobar que el antiguo broker está detenido.
**No afirmamos que ya se ejecutaron:** solo hemos validado sintaxis/código localmente.

## 4. Si aparece un error nuevo

```bash
printenv ROS_DOMAIN_ID
which ros2
ros2 pkg prefix arm_broker
ros2 interface show arm_broker_interfaces/action/MoveArm
ros2 node list
ros2 action list -t
ros2 topic info /joint_states -v
```

Si los tipos siguen confundidos, abre terminal completamente nueva y carga SOLO ROS Humble
+ `~/logistica/install/setup.bash`. NO encadenar `source ~/rb2_ws/install/...` ni
`source ~/jetcobot_ws/install/...` para ejecutar este proyecto.
