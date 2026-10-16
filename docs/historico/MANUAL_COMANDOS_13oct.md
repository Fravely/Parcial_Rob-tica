# Manual de comandos — Gran Reto JetCobot

Comandos por máquina para el examen parcial. Cada bloque se copia tal cual; lo que hay que
reemplazar va en MAYÚSCULAS (`IP_DOCENTE`, `PUERTO`, `PRESET`).

**Datos del equipo (confirmar el día del examen)**

| Qué | Valor de práctica | Valor del examen |
|---|---|---|
| Jetson (JetCobot) | `172.51.9.15` · usuario `jetson` | mismo |
| JupyterLab del Jetson | `http://172.51.9.15:8888` | mismo |
| `ROS_DOMAIN_ID` | `52` | el asignado al equipo |
| Servidor LAYA (Windows del laboratorio) | `http://172.51.1.2:8000` · preset `multilingual` | `http://IP_DOCENTE:PUERTO` · `PRESET` |
| Workspace | `~/logistica` | mismo |
| Puerto del brazo | `/dev/ttyUSB0` a `1000000` baudios | mismo |

**Regla que no se negocia:** un solo broker, un solo intérprete y un solo `move_group`
corriendo a la vez. Casi todos los errores raros de este proyecto vienen de tener dos.

---

## 0. Mapa: qué corre en cada máquina

| Máquina | Qué corre | Pregunta |
|---|---|---|
| **Jetson** | `interprete_ordenes`, `arm_broker`, `move_group`, `transcriptor_voz`, `interfaz_ordenes`, `ros2 bag` | 1, 2 y 3 |
| **Windows del laboratorio** | servidor LAYA (HTTP, no es nodo ROS 2) | 1 |
| **Raspberry Pi × 4** | un cliente por integrante: `orden_a_recogida` o el navegador | 2 |
| **Internet (Google AI Studio)** | transcripción de voz | 3 |

El brazo lo mueve **solo** el worker del broker, que corre en el Jetson. Ninguna Raspberry
ni ninguna PC abre el puerto serie.

---

## 1. Jetson (JetCobot)

### 1.1 Abrir una terminal limpia (SIEMPRE lo primero)

En JupyterLab (`http://172.51.9.15:8888`) → *File → New → Terminal*. En **cada** terminal
nueva, antes que nada:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
export ROS_LOCALHOST_ONLY=0        # las Raspberry deben ver este grafo
cd ~/logistica
source install/setup.bash          # después de compilar al menos una vez
```

No encadenar `source ~/rb2_ws/install/setup.bash` ni `~/jetcobot_ws/install/setup.bash`:
esos workspaces traen otra versión de `MoveArm.action` y las dos no son intercambiables.

### 1.2 Comprobar que no hay procesos viejos

```bash
ros2 node list
ros2 action list -t
pgrep -af 'broker|interprete|move_group|jupyter.*kernel' | head -20
fuser -v /dev/ttyUSB0              # tiene que salir VACÍO antes de arrancar el broker
```

Si aparece otro broker o intérprete, se para con `Ctrl+C` en su terminal, o:

```bash
kill -INT PID                      # PID de la lista anterior; nunca kill -9 con el brazo activo
```

Si `/dev/ttyUSB0` está ocupado por un notebook, cerrar ese kernel en JupyterLab
(*Kernel → Shut Down Kernel*), no basta con cerrar la pestaña.

### 1.3 Instalar el proyecto y compilar

```bash
cd ~
unzip -o logistica.zip             # o subir la carpeta por JupyterLab
cd ~/logistica
colcon list --names-only           # arm_broker, arm_broker_interfaces, laya_ordenes, laya_ordenes_interfaces
colcon build --symlink-install
source install/setup.bash
ros2 pkg executables arm_broker laya_ordenes
```

Debe listar: `arm_broker broker`, `arm_broker cliente`, `laya_ordenes interprete_ordenes`,
`laya_ordenes orden_a_broker`, `laya_ordenes orden_a_recogida`, `laya_ordenes interfaz_ordenes`,
`laya_ordenes transcriptor_voz`.

Comprobar que las interfaces son las de este proyecto:

```bash
ros2 interface show arm_broker_interfaces/action/PickPlace    # debe traer accion, objeto, color, zona
ros2 interface show arm_broker_interfaces/action/MoveArm      # debe decir joint_positions, NO q_deseado
ros2 interface show laya_ordenes_interfaces/srv/InterpretarOrden
```

### 1.4 Pruebas sin robot (hacerlas antes de tocar el brazo)

```bash
cd ~/logistica
python3 -m unittest discover -s tests -v
python3 herramientas/probar_broker_sin_ros.py        # cola, exclusión mutua, FIFO, prioridad
python3 herramientas/probar_item2_sin_robot.py       # montaje, admisión, plan, fallos, evidencia
python3 herramientas/diagnostico_item2.py > evidencias/diagnostico_item2.txt 2>&1
cat evidencias/diagnostico_item2.txt
```

El diagnóstico no abre el puerto ni mueve nada. De su salida se sacan los nombres reales
del grupo, el enlace y el marco de MoveIt (`arm_group`, `6_Link`, `base_link` son valores
por defecto que **hay que confirmar**).

### 1.5 Pregunta 1 — intérprete de órdenes

**Terminal A** (dejarla abierta todo el examen):

```bash
ros2 run laya_ordenes interprete_ordenes --ros-args -r __node:=interprete_ordenes \
  -p url_laya:=http://IP_DOCENTE:PUERTO \
  -p modelo_laya:=PRESET \
  -p timeout_s:=2.0 \
  -p objetos_disponibles:="['cubo']" \
  -p colores_disponibles:="['rojo','azul','verde','amarillo']" \
  -p registro_csv:=$HOME/logistica/evidencias/pregunta1/interpretaciones.csv
```

El inventario debe ser **exactamente lo que está sobre la mesa**.

Probar desde otra terminal:

```bash
ros2 service call /interpretar_orden laya_ordenes_interfaces/srv/InterpretarOrden \
  "{frase: 'recoge el cubo rojo urgente'}"
ros2 param get /interprete_ordenes url_laya
ros2 param get /interprete_ordenes timeout_s
```

Con LAYA real debe responder `fuente='LAYA'` y `degradada=False`.

Las 50 frases y las tablas de latencia y exactitud:

```bash
python3 herramientas/evaluar_pregunta1.py --modo calma \
  --entrada evidencias/pregunta1/50_frases_docente.csv \
  --salida evidencias/pregunta1/calma.csv --timeout 10
# repetir con --modo carga mientras todos los equipos consultan a la vez
```

### 1.6 Pregunta 2 — broker

Los tres modos son excluyentes y por defecto **no se mueve nada**.

**Ensayo sin cámara ni brazo** (sirve para probar la cola con los cuatro integrantes):

```bash
ros2 run arm_broker broker --ros-args --params-file plantillas/item2_simulado.yaml
```

**Solo planificación** (IK y trayectoria de MoveIt2, nunca ejecuta):

```bash
ros2 run arm_broker broker --ros-args \
  -p habilitar_planificacion_pick_place:=true \
  -p inventario_pick_place:="['cubo:rojo','cubo:azul','cubo:verde','cubo:amarillo']" \
  -p objetivos_planificacion_json:='{"cubo:rojo@deposito":[160,56,123,0,0,0]}'
```

**Antes del modo físico**, marcar las regiones de la cámara y revisar los planes:

```bash
# 1) imagen desde la pose de escaneo (con supervisión), descargarla y marcarla en una
#    laptop con escritorio y OpenCV:
python3 herramientas/marcar_regiones_item2.py --imagen escaneo.png \
  --config plantillas/item2_montaje.json --salida plantillas/item2_calibrado.json

# 2) de vuelta en el Jetson, con move_group corriendo:
python3 herramientas/previsualizar_item2.py --config plantillas/item2_calibrado.json \
  --color rojo --salida evidencias/plan_rojo.json
# repetir con azul, verde y amarillo

# 3) solo si los cuatro planes son razonables:
#    editar plantillas/item2_calibrado.json y poner  "montaje_validado": true
```

**Demostración evaluada (modo físico).** Antes: `fuser -v /dev/ttyUSB0` vacío, `move_group`
corriendo como planificador y el driver RB-2 detenido.

```bash
mkdir -p evidencias/item2
ros2 run arm_broker broker --ros-args --params-file plantillas/item2_fisico.yaml \
  -p config_item2:="$(pwd)/plantillas/item2_calibrado.json" \
  -p habilitar_pick_place_fisico:=true
```

Evidencia mientras trabajan los cuatro integrantes (otra terminal):

```bash
ros2 bag record --include-hidden-topics -o evidencias/item2/bag_demo \
  /arm/queue_state /arm/measured_joint_states /interfaz/ordenes \
  /pick_place/_action/feedback /pick_place/_action/status /rosout
```

Prueba del publicador único, durante la demostración:

```bash
fuser -v /dev/ttyUSB0          # un solo proceso: el broker
ros2 topic info /joint_states -v
ros2 node list                 # un solo arm_broker
```

Tabla de los diez intentos, al terminar:

```bash
python3 herramientas/resumen_item2.py evidencias/item2/intentos.csv \
  --crear-revision evidencias/item2/revision_video.csv
# completar objeto_correcto, zona_correcta y evidencia mirando el video
python3 herramientas/resumen_item2.py evidencias/item2/intentos.csv \
  --revision evidencias/item2/revision_video.csv
```

### 1.7 Pregunta 3 — voz e interfaz web

```bash
# clave de Google, fuera del repositorio
nano ~/.clave_gemini            # una línea:  export GEMINI_API_KEY="AIza..."
chmod 600 ~/.clave_gemini
source ~/.clave_gemini
python3 -c "import os; print('CLAVE OK' if os.getenv('GEMINI_API_KEY') else 'FALTA')"

arecord -l                      # anotar card y device del micrófono
ros2 run laya_ordenes transcriptor_voz --ros-args \
  -p enviar_al_broker:=true -p client_id:=voz \
  -p timeout_transcripcion_s:=6.0 -p dispositivo_alsa:=plughw:2,0 \
  -p dir_evidencias:=$HOME/logistica/evidencias/pregunta3

# interfaz web para escribir el prompt (opcional, útil también en la P2)
ros2 run laya_ordenes interfaz_ordenes --ros-args -p puerto_web:=8090 \
  -p registro_csv:=$HOME/logistica/evidencias/interfaz/ordenes_interfaz.csv
```

El detalle de la Pregunta 3 (modo texto sin internet, desglose de tiempos, las cinco
órdenes) está en `docs/GUIA_PREGUNTA3.md`.

---

## 2. Windows de la máquina del laboratorio

Todo se escribe en **PowerShell** (no en una terminal de Linux). El servidor LAYA vive
aquí: es HTTP, **no** es un nodo ROS 2 y no aparece en `ros2 node list`.

### 2.1 Si el docente ya lo dejó corriendo (caso normal del examen)

```powershell
ipconfig                                        # anotar la IPv4 de la máquina
Get-NetTCPConnection -LocalPort 8000 -State Listen
curl.exe http://127.0.0.1:8000/health
```

`/health` debe responder algo como
`{"status":"ok","loaded":["multilingual"],"device":"cpu"}`.
Ese `loaded` es el **preset** que va en `-p modelo_laya:=`.

### 2.2 Abrir el puerto en el firewall (si el Jetson no llega)

Sin esto, LAYA funciona en la propia máquina pero el Jetson recibe *timeout*. Requiere
PowerShell **como administrador**:

```powershell
New-NetFirewallRule -DisplayName "LAYA 8000" -Direction Inbound -Protocol TCP `
  -LocalPort 8000 -Action Allow
```

### 2.3 Comprobar que el Jetson y Windows se ven

```powershell
Test-NetConnection 172.51.9.15 -InformationLevel Detailed
```

Y desde el Jetson, al revés:

```bash
ping -c 4 IP_DOCENTE
curl -sS --max-time 5 http://IP_DOCENTE:PUERTO/health
```

---

## 3. Manual: cómo activar LAYA

Solo hace falta si el servidor **no** está corriendo. El examen dice que ningún equipo
instala ni entrena modelos, así que esto es el procedimiento de respaldo (y es el que ya
ejecutaron en la práctica).

### 3.1 Instalación (una sola vez)

```powershell
python --version                 # 3.14.3 en la máquina del laboratorio
py -0p                           # lista los Python instalados

py -3.14 -m venv "$env:USERPROFILE\laya-servidor-venv"
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -m pip install --upgrade pip
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -m pip install "laya[serve]"
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -m pip show laya
```

### 3.2 Arrancar el servidor

```powershell
$env:LAYA_HOST="0.0.0.0"          # 0.0.0.0 = acepta conexiones del Jetson; 127.0.0.1 NO
$env:LAYA_PORT="8000"
$env:LAYA_DEVICE="cpu"            # 'auto' lo rechaza; ver 3.3 para usar la GPU
$env:LAYA_MODELS="multilingual"
$env:LAYA_DEFAULT_MODEL="multilingual"
$env:LAYA_PRELOAD="1"             # carga el modelo al arrancar, no en la primera petición
& "$env:USERPROFILE\laya-servidor-venv\Scripts\laya-serve.exe"
```

Esa ventana se queda ocupada: **no cerrarla**. La primera carga del modelo tarda; hasta
que termine, `/health` puede no responder.

### 3.3 Usar la GPU (opcional, reduce el tiempo de inferencia)

La máquina del laboratorio tiene tarjeta gráfica, pero LAYA solo la usa si PyTorch se
instaló con CUDA. Comprobar primero:

```powershell
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"
```

- Si imprime `True` → se puede arrancar con `$env:LAYA_DEVICE="cuda"`.
- Si imprime `False` → **dejarlo en `cpu`**. Reinstalar PyTorch con CUDA el día del examen
  es media hora y puede dejar el servidor inservible. En la práctica, con CPU, la
  inferencia fue de ~121 ms de mediana: suficiente.

### 3.4 Verificar desde otra ventana de PowerShell

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
curl.exe http://127.0.0.1:8000/health
```

### 3.5 Verificar desde el Jetson

```bash
curl -sS --max-time 5 http://IP_DOCENTE:PUERTO/health
curl -v --connect-timeout 5 http://IP_DOCENTE:PUERTO/v1/systemone   # un GET puede dar 405: es normal
```

`405 Method Not Allowed` confirma que el servidor está ahí: `/v1/systemone` solo acepta
POST. Lo que **no** se puede hacer es adivinar otro puerto.

### 3.6 Apagar

`Ctrl+C` en la ventana del servidor. Para comprobar que soltó el puerto:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen   # no debe devolver nada
```

---

## 4. Raspberry Pi (los cuatro clientes de la Pregunta 2)

Cada integrante manda sus órdenes desde su Raspberry. Hay dos caminos; **el A es el que
demuestra mejor la regla del RB-2** (cuatro clientes ROS 2 distintos en el grafo).

Antes de elegir, mirar qué sistema tiene la Raspberry:

```bash
lsb_release -a
uname -m
```

- **Ubuntu 22.04 (arm64)** → camino A (ROS 2 Humble tiene paquetes binarios).
- **Raspberry Pi OS / Debian** → camino B. Compilar ROS 2 desde fuente en una Raspberry
  toma horas: no se intenta el día del examen.

### 4.1 Camino A — cliente ROS 2 en cada Raspberry

**Una sola vez, por Raspberry:**

```bash
sudo apt update && sudo apt install -y software-properties-common curl gnupg lsb-release
sudo add-apt-repository universe -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install -y ros-humble-ros-base python3-colcon-common-extensions
```

**Copiar SOLO las interfaces** (son las que deben coincidir byte a byte con el Jetson) y
el cliente. Desde la Raspberry:

```bash
mkdir -p ~/cliente_ws/src && cd ~/cliente_ws
scp -r jetson@172.51.9.15:~/logistica/src/arm_broker_interfaces src/
scp -r jetson@172.51.9.15:~/logistica/src/laya_ordenes_interfaces src/
scp jetson@172.51.9.15:~/logistica/src/laya_ordenes/laya_ordenes/orden_a_recogida.py ~/

source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

**Cada vez que se abre una terminal en la Raspberry:**

```bash
source /opt/ros/humble/setup.bash
source ~/cliente_ws/install/setup.bash
export ROS_DOMAIN_ID=52           # EL MISMO del Jetson
export ROS_LOCALHOST_ONLY=0
```

**Comprobar que la Raspberry ve el grafo del Jetson:**

```bash
ros2 node list                    # deben aparecer arm_broker e interprete_ordenes
ros2 action list -t | grep pick_place
ros2 interface show arm_broker_interfaces/action/PickPlace
```

Si `ros2 node list` sale vacío: están en redes distintas, el `ROS_DOMAIN_ID` no coincide o
la Wi-Fi del laboratorio bloquea multicast (ver el cuadro de errores).

**Enviar una orden (cada integrante con su propio `client_id`):**

```bash
python3 ~/orden_a_recogida.py --ros-args \
  -p client_id:=sebastian \
  -p frase:='recoge el cubo rojo urgente' \
  -p zona:=deposito \
  -p enviar_pedido:=true
```

La prioridad **no se escribe a mano**: el cliente copia la que devolvió el intérprete.
Para la demostración evaluada no se añade `-p permitir_respaldo:=true` (eso solo sirve
para ensayar sin LAYA).

El cliente imprime la decisión, la posición en la cola y el resultado:

```
DECISION: recoger cubo rojo; prioridad=68; permitido=True; fuente=LAYA
QUEUED: cola=2, t=0.41s
MOVER_PREAGARRE: cola=0, t=12.80s
RESULTADO: success=True; verificado_fisico=True; DEPOSITO VERIFICADO...
```

### 4.2 Camino B — navegador (sin ROS en la Raspberry)

Con `interfaz_ordenes` corriendo en el Jetson, cada Raspberry solo necesita Chromium:

```
http://172.51.9.15:8090
```

Cada integrante escribe su nombre en *Integrante (client_id)* y su orden. La página
muestra la decisión, la cola del broker en vivo y el estado de cada pedido.

**Qué se pierde:** los cuatro pedidos entran al grafo desde un único nodo
(`interfaz_ordenes`), aunque cada uno conserve su `client_id`. Si el docente pide ver
cuatro clientes ROS 2 distintos, hay que usar el camino A. Si se usa el camino B, decirlo
en el informe tal cual.

Si la página no abre desde la Raspberry:

```bash
ping -c 3 172.51.9.15
curl -sS http://172.51.9.15:8090/api/estado | head -c 200
```

Y en el Jetson:

```bash
ss -ltnp | grep 8090              # debe escuchar en 0.0.0.0:8090
sudo ufw allow 8090               # solo si hay firewall activo
```

### 4.3 Las cuatro órdenes en paralelo

Para la demostración, los cuatro ejecutan su comando **a la vez** (contar «3, 2, 1»). En
el Jetson se ve una sola ejecución y tres en espera:

```bash
ros2 topic echo /arm/queue_state --once
```

---

## 5. Orden del día del examen

| # | Dónde | Qué |
|---|---|---|
| 1 | Windows | Confirmar LAYA: `/health` responde y anotar IP, puerto y preset |
| 2 | Jetson | Terminal limpia, `fuser -v /dev/ttyUSB0` vacío, `ros2 node list` sin duplicados |
| 3 | Jetson | `colcon build` + `source install/setup.bash` + `ros2 interface show PickPlace` |
| 4 | Jetson | **Terminal A**: intérprete con la IP del docente. Probar una frase |
| 5 | Jetson | Escribir las **predicciones** antes de medir |
| 6 | Jetson | Las 50 frases en calma y bajo carga (Pregunta 1) |
| 7 | Jetson | `move_group`, marcar regiones, previsualizar planes, `montaje_validado: true` |
| 8 | Jetson | **Terminal B**: broker en modo físico. **Terminal C**: `ros2 bag record` |
| 9 | Raspberry × 4 | Los diez intentos, cuatro clientes en paralelo (Pregunta 2) |
| 10 | Jetson | **Terminal D**: transcriptor de voz; las cinco órdenes dictadas (Pregunta 3) |
| 11 | Jetson | Modo texto con internet bloqueado (ver `docs/GUIA_PREGUNTA3.md` §3.4) |
| 12 | Jetson | `resumen_item2.py` y `desglose_tiempos.py`; cerrar el bag |
| 13 | Cualquiera | `git grep -n AIza` vacío, `git push`, enlace al aula virtual |

---

## 6. Cuadro de errores

### 6.1 Compilación y entorno (Jetson)

| Mensaje | Causa | Solución |
|---|---|---|
| `colcon ERROR: Duplicate package names` | Una copia del proyecto dentro del workspace | `touch CARPETA_COPIA/COLCON_IGNORE` y recompilar |
| `Package 'arm_broker' not found` | No se hizo `source install/setup.bash` o se compiló otro workspace | `cd ~/logistica && colcon build && source install/setup.bash` |
| `ros2 interface show` dice `q_deseado` | Está cargado el `arm_broker_interfaces` de `~/rb2_ws` | Terminal NUEVA, cargar solo `/opt/ros/humble` y `~/logistica/install` |
| `AttributeError: joint_positions` / `q_deseado` | Dos versiones de `MoveArm.action` mezcladas en el mismo dominio | Parar el broker equivocado; `ros2 interface show` antes de empezar |
| `ModuleNotFoundError: moveit_msgs` | Falta MoveIt 2 (solo lo necesitan los modos plan y físico) | `sudo apt install ros-humble-moveit-msgs`; para simular no hace falta |
| `ModuleNotFoundError: cv2` | Falta OpenCV | `sudo apt install python3-opencv` |
| `ros2 action list -t` vacío | El broker no está corriendo o hay otro `ROS_DOMAIN_ID` | `echo $ROS_DOMAIN_ID` y arrancar el broker |

### 6.2 Arranque del broker

| Mensaje | Causa | Solución |
|---|---|---|
| `elige UN modo de PickPlace: simulado, planificacion o fisico` | Dos banderas de modo en `true` | Dejar una sola; las `--ros-args` ganan sobre el `--params-file` |
| `PickPlace requiere publicar_joint_states=false` | `publicar_joint_states:=true` con PickPlace | Quitarlo: en modo físico los comandos van por el puerto serie, no por el tópico |
| `montaje pendiente: revisar modelo, aproximaciones y regiones` | `montaje_validado` sigue en `false` | Marcar regiones, previsualizar planes y recién entonces ponerlo en `true` |
| `faltan regiones: ...` | El JSON no tiene las regiones de los cuatro cubos y del depósito | `marcar_regiones_item2.py` y usar el JSON calibrado |
| `regiones solapadas: X y Y` | Dos rectángulos se tocan | Volver a marcar más ajustado al lugar de agarre |
| `region fuera de imagen: X` | Las regiones se marcaron con otra resolución | Marcar sobre la imagen real de la cámara (misma resolución de todo el ensayo) |
| `valor fuera de rango: velocidad_brazo` | Valor fuera de los límites del JSON | Respetar los rangos (`velocidad_brazo` 1–35, pinza 0–100) |
| `MONTAJE: ... 3_Joint a 1.0 grados de su limite` (aviso) | La pose de depósito está al borde del rango articular | Reenseñar esa pose con más margen, o la aproximación fallará |
| `MONTAJE: deposito_grados es UNA sola pose...` (aviso) | Los cuatro cubos van al mismo punto | Usar recipiente, o poner `deposito_grados` como objeto con una pose por color |
| `COHERENCIA FK: arm_broker/fk.py tiene OTRA tabla DH` | Alguien editó `fk.py` y no `broker.py` (o al revés) | Dejar las dos tablas iguales: si no, el error en mm del informe no significa nada |

### 6.3 Puerto serie y brazo

| Mensaje | Causa | Solución |
|---|---|---|
| `el puerto /dev/ttyUSB0 ya esta ocupado` | Otro broker, un notebook o el driver RB-2 lo tienen | `fuser -v /dev/ttyUSB0`, cerrar ese proceso o el kernel de Jupyter |
| `falta el comando fuser` | No está `psmisc` | `sudo apt install psmisc` |
| `otro proceso de este broker ya tiene el puerto` | Quedó un broker zombi | `pgrep -af broker` y cerrarlo |
| `el brazo no devolvio seis angulos` | Cable, baudrate o el brazo apagado | Revisar el cable, `baudios: 1000000`, encender el brazo |
| `el brazo no alcanzo el punto N/M del plan (error X grados)` | Tolerancia muy fina, velocidad baja o choque | Subir `tolerancia_intermedia_grados` (3–5), revisar que no haya obstáculo |
| `el controlador rechazo el punto articular` | pymycobot devolvió −1 | Revisar la versión de pymycobot que ya funcionaba en los notebooks |
| `plan demasiado disperso para reproducir por puntos` | MoveIt devolvió saltos grandes entre puntos | Subir `salto_maximo_plan_grados` o replanificar con otra semilla |
| `brazo enclavado por un fallo de hardware anterior` | Hubo un fallo serio y el broker se cerró a propósito | Revisar el brazo **a mano**, después reiniciar el broker |
| `lectura fisica fuera del worker` | Alguien llamó al hardware desde otro hilo | No tocar: es la defensa de la regla del publicador único |

### 6.4 Visión y pedidos

| Mensaje | Causa | Solución |
|---|---|---|
| `el cubo COLOR no esta (o no es estable) en su posicion fija` | El cubo no está, o está fuera de su región | Es un **intento fallido**, no un fallo del broker: colocar el cubo y reenviar |
| `el deposito ya contiene ese color` | Quedó un cubo de la tanda anterior | Vaciar el depósito entre tandas, con el sistema detenido |
| `no se confirmo la desaparicion del origen y la aparicion en el deposito` | El agarre falló o la cámara no lo vio | Revisar el video antes de contarlo como éxito; el CSV guarda el intento |
| `la camara no respondio en 15 segundos` | Cámara ocupada o desconectada | Cerrar notebooks que usen la cámara; `ls /dev/video*` |
| `resolucion distinta de la usada para marcar regiones` | La cámara cambió de resolución | Volver a marcar las regiones con la resolución real |
| `accion "detener" no admitida` | La orden no es de manipulación | Correcto: se rechaza antes de encolar |
| `respuesta degradada y el respaldo no esta habilitado` | LAYA no respondió y el modo evaluado exige LAYA | Revisar LAYA; para ensayar, `-p permitir_respaldo_pick_place:=true` |
| `objeto/color no incluido en el inventario configurado` | El inventario del broker no coincide con la mesa | Ajustar `inventario_pick_place` |
| `cola llena (maximo 20)` | Más de 20 pedidos esperando | Esperar; o subir `cola_max` |
| `MoveArm deshabilitado durante PickPlace fisico` | Se usó el cliente viejo en modo físico | Usar `orden_a_recogida` (acción `/pick_place`) |

### 6.5 MoveIt 2

| Mensaje | Causa | Solución |
|---|---|---|
| `servicio MoveIt2 no disponible` | `move_group` no corre, o hay dos | `ros2 node list \| grep move_group`: debe haber **uno** |
| `FK RB2 y URDF difieren X mm` | El enlace o el marco de MoveIt no son los del RB-2 | Ajustar `moveit_grupo`, `moveit_enlace`, `moveit_marco` con la salida del diagnóstico |
| `IK fallo, codigo MoveIt2=-31` | La pose está fuera de alcance o en colisión | Revisar la pose enseñada y la altura de aproximación |
| `planificacion fallo, codigo MoveIt2=-1` | No encontró trayectoria | Revisar obstáculos en la escena y el estado inicial |
| `IK eligio otra rama distinta de la pose ensenada` | La IK dio una solución con el codo al otro lado | Es una defensa: reenseñar la pose o revisar la semilla |
| `trayectoria no comienza en el estado solicitado` | El estado inicial no es el del brazo | En modo físico se lee del brazo; revisar que no haya otro publicador de estado |

### 6.6 Red, LAYA y las Raspberry

| Síntoma | Causa | Solución |
|---|---|---|
| `TimeoutError: LAYA superó timeout_s=2.00` | LAYA no responde a tiempo | `curl .../health` desde el Jetson; revisar IP, puerto y firewall |
| `curl: (28) Connection timed out` | Firewall de Windows o IP equivocada | Regla de entrada para el puerto (§2.2); `ipconfig` en Windows |
| `curl: (7) Connection refused` | LAYA no está corriendo o escucha en `127.0.0.1` | Arrancar con `LAYA_HOST=0.0.0.0` |
| `405 Method Not Allowed` en `/v1/systemone` | Se hizo un GET | Normal: ese endpoint es POST. Confirma que el servidor está vivo |
| `curl: (3) URL using bad/illegal format` | El comando se partió con `\` mal puesto | Escribirlo en **una sola línea** |
| `Get-NetTCPConnection: command not found` | Comando de PowerShell en bash | Ejecutarlo en Windows |
| `ros2 node list` vacío en la Raspberry | `ROS_DOMAIN_ID` distinto, otra red o multicast bloqueado | Igualar el dominio; `export ROS_LOCALHOST_ONLY=0`; conectar por cable si la Wi-Fi bloquea multicast |
| La Raspberry ve los nodos pero el goal nunca se acepta | Interfaces compiladas de distinta fuente | Volver a copiar `arm_broker_interfaces` del Jetson y recompilar |
| `no aparece /interpretar_orden` | El intérprete está caído o en otro dominio | Terminal A del Jetson |
| `http://IP:8090` no abre | La interfaz no corre, o firewall | `ss -ltnp \| grep 8090` en el Jetson |

### 6.7 Pregunta 3 (voz)

| Mensaje | Causa | Solución |
|---|---|---|
| `arecord: command not found` | Falta ALSA | `sudo apt install alsa-utils` |
| `arecord no genero audio` | Dispositivo equivocado | `arecord -l` y `-p dispositivo_alsa:=plughw:X,Y` |
| `GEMINI_API_KEY no configurada` | No se hizo `source ~/.clave_gemini` | Hacerlo en esa terminal |
| `HTTP 400 ... API key not valid` | Clave mal copiada | Regenerar en Google AI Studio |
| `HTTP 429` | Cuota gratuita agotada | Otra clave del equipo, o esperar |
| `HTTP 404 ... model not found` | Nombre de modelo | `-p modelo_gemini:=gemini-3.6-flash` |
| `transcripcion vacia` | Audio bajo, o el modelo devolvió nada | Hablar cerca del micrófono; el nodo ya prueba el modelo de respaldo |
| `MODO TEXTO POR TECLADO — ConnectionError` | Sin internet | Es el comportamiento exigido: escribir la orden y seguir |

---

## 7. Comandos de emergencia

```bash
# parar todo sin dejar el brazo a medias
# 1) Ctrl+C en la terminal del broker (ordena la parada del brazo y cierra el puerto)
# 2) comprobar que soltó el puerto:
fuser -v /dev/ttyUSB0

# el brazo quedó en una pose rara: moverlo a mano NO, con el brazo energizado
# reiniciar el broker y enviar un pedido; la secuencia empieza yendo a escaneo

# matar un broker zombi
pgrep -af 'arm_broker|broker.py'
kill -INT PID          # esperar 5 s; solo si no responde, kill -9

# ver quién publica en el tópico del brazo
ros2 topic info /joint_states -v
ros2 topic info /arm/measured_joint_states -v

# limpiar evidencias de una sesión fallida (NO borrar fallos de una sesión válida)
mv evidencias/item2 evidencias/item2_descartada_$(date +%H%M)
```
