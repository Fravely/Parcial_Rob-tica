# Manual de comandos — Pregunta 2 con LAYA

_Agarre autónomo bajo la cola del broker: voz escrita → LAYA → cola RB-2 → cámara → IK/MoveIt2 → pinza_

| Dato | Valor |
|---|---|
| JetCobot (Jetson) | `172.51.1.18` · usuario `jetson` · carpeta `/home/jetson/logistica` |
| JupyterLab | `http://172.51.1.18:8888` (cada integrante lo abre desde su laptop) |
| ROS_DOMAIN_ID | `72` (lo fija `scripts/entorno.sh` en cada terminal) |
| Servidor LAYA (PC Windows) | IP, puerto y preset que dicta el docente. Práctica: `http://172.51.1.2:8000`, preset `multilingual` |
| Acción del broker | `/logistica/pick_place` (cola: `/logistica/arm/queue_state`) |
| Brazo | `/dev/ttyUSB0` a 1 000 000 baudios · velocidad 35 · pinza 100/15 |
| Evidencias | `evidencias/pregunta2/` (intentos.csv, rechazos.csv, bag, capturas) |

> **Cómo usar este manual:** cada bloque gris se copia tal cual en una terminal de JupyterLab (File → New → Terminal). Lo que va en MAYÚSCULAS (IP_DOCENTE, PUERTO, PRESET) se reemplaza por el dato del docente. El orden de las terminales importa: MoveIt → broker → intérprete → bag → clientes.

## 1. Qué cambió con la fusión y qué corre dónde

La carpeta `logistica` ahora contiene **el broker que ya funcionó físicamente en `logistica_sinLaya1`** (mismo `broker.py`, mismas poses, misma secuencia escaneo → cámara → agarre → depósito) **más los paquetes de LAYA reactivados** (`laya_ordenes`, `laya_ordenes_interfaces`). La diferencia con la prueba sin LAYA es solo el origen de la decisión: antes la escribían reglas locales; ahora la produce el servicio `/interpretar_orden`, que consulta a LAYA y, si LAYA no responde a tiempo, usa el clasificador por palabras clave (respuesta marcada como degradada).

| Antes (logistica_sinLaya1) | Ahora (logistica fusionada) | Por qué |
|---|---|---|
| Acción `/sin_laya/pick_place` | Acción `/logistica/pick_place` | El nombre ya no contradice que se usa LAYA |
| `bash scripts/cliente.sh integranteN` (reglas locales) | `bash scripts/cliente.sh integranteN` → **LAYA**; el modo local queda en `scripts/cliente_sin_laya.sh` | La prioridad sale del modelo (requisito 1) |
| Prioridad local 1/2/3, τ = 8 s | Prioridad del modelo (LAYA: score×50 ≈ 59–86; respaldo 20/80/180), τ = 0,2 s | Una sola escala para LAYA, respaldo y modo local; 50 puntos ≈ 10 s de espera |
| Paquetes LAYA con `COLCON_IGNORE` | Se compilan los 4 paquetes | Intérprete, cliente LAYA y transcriptor (P3) |
| Solo acción `recoger` | `recoger` y `colocar` | "lleva/deposita el cubo X" es la misma tarea física |
| `config/poses_sin_laya.json`, `broker_sin_laya.yaml` | `config/poses.json`, `config/broker.yaml` | Mismos valores; nombres neutros |
| `evidencias/sin_laya/` | `evidencias/pregunta2/` | Ordenado por pregunta del examen |

### Mapa de terminales (todas en el Jetson, por JupyterLab)

| Terminal | Qué corre | Comando | Señal de que está bien |
|---|---|---|---|
| A | MoveIt2 solo planificador | `bash scripts/moveit.sh` | `You can start planning now!` |
| B | Broker RB-2 (único worker) | `bash scripts/broker.sh` | `arm_broker listo · política=prioridad · modo=fisico` |
| C | Intérprete (único que habla con LAYA) | `bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET` | `Servicio /interpretar_orden listo. URL=http://…` |
| D | Grabación ros2 bag | `bash scripts/grabar.sh p2` | `Subscribed to topic …/queue_state` |
| E–H | Un cliente por integrante | `bash scripts/cliente.sh integrante1` … `integrante4` | `Cliente LAYA listo.` y el prompt `integrante1>` |
| I (opcional) | Ver la cola en vivo (para el video) | `bash scripts/ver_cola.sh` | Mensajes `QueueState` a 5 Hz |

> **Nota:** todas las terminales empiezan con `cd ~/logistica`. Los scripts ya cargan ROS 2 Humble, `ROS_DOMAIN_ID=72` y el `install/` del proyecto: no hace falta escribir `source …` a mano. No se debe cargar `~/rb2_ws` ni `~/jetcobot_ws` en estas terminales.

## 2. Subir el proyecto al Jetson y compilar (una sola vez)

#### 2.1 En la laptop (Windows)

1. Comprimir la carpeta `C:\Users\ASUS\Downloads\logistica_final\logistica` (clic derecho → Comprimir en archivo ZIP) y llamarla `logistica.zip`. Si se puede, borrar antes sus carpetas `build`, `install` y `log` (se regeneran en el Jetson).
2. Abrir `http://172.51.1.18:8888`, ir a la carpeta de inicio (`/home/jetson`) y subir `logistica.zip` con el botón de subir archivos.

#### 2.2 En una terminal de JupyterLab

**Descomprimir y compilar**

```bash
cd ~
# si ya existe una carpeta logistica vieja, se guarda con otro nombre (no se borra)
[ -d ~/logistica ] && mv ~/logistica ~/logistica_old_$(date +%m%d_%H%M)
unzip -q logistica.zip
ls ~/logistica/scripts          # debe listar broker.sh, cliente.sh, interprete.sh, voz.sh ...
cd ~/logistica
sed -i "s/\r$//" scripts/*.sh   # por si Windows cambió los fines de línea
bash scripts/compilar.sh --limpio
```

> **Resultado esperado:** termina con `Summary: 4 packages finished` y lista los ejecutables `broker`, `cliente`, `cliente_sin_laya`, `interprete_ordenes`, `cliente_laya`, `transcriptor_voz`, `interfaz_ordenes`, `orden_a_recogida`, `orden_a_broker`.

**Comprobaciones sin mover el robot**

```bash
source scripts/entorno.sh
ros2 interface show arm_broker_interfaces/action/PickPlace | head -9   # client_id, priority, accion, objeto, color, zona, permitido, degradada, fuente
ros2 interface show laya_ordenes_interfaces/srv/InterpretarOrden
python3 -m unittest discover -s tests -v                 # 20 pruebas OK
python3 herramientas/probar_broker_sin_ros.py             # TODO OK (cola, exclusión, FIFO, prioridad)
python3 herramientas/pruebas_sin_ros/prueba_cliente_laya.py   # PRUEBA cliente_laya: OK
```

## 3. Antes de encender nada: checklist del turno

- Es el turno del grupo y el brazo y la cámara están libres. **No cerrar procesos de otro grupo.**
- Cerrar los procesos propios de `logistica_sinLaya1` (broker y MoveIt): Ctrl+C en sus terminales. El broker nuevo se niega a arrancar si el anterior sigue abierto.
- Ningún notebook usando el brazo o la cámara: en JupyterLab, *Kernel → Shut Down Kernel* (cerrar la pestaña no basta).
- Cuatro cubos (amarillo, azul, verde, rojo) en las cuatro posiciones fijas; el encuadre de la cámara no se movió. Los colores pueden intercambiarse de lugar.
- Punto de depósito libre o con el recipiente previsto (los cuatro pedidos dejan el cubo en la misma pose).
- Escribir **las predicciones** antes de medir (tasa de éxito esperada, orden esperado de atención, error en mm esperado).

**Comprobaciones previas**

```bash
cd ~/logistica && source scripts/entorno.sh
echo $ROS_DOMAIN_ID                 # 72
ros2 node list                      # sin otro arm_broker, interprete_ordenes ni move_group
fuser -v /dev/ttyUSB0               # VACÍO: nadie tiene el puerto del brazo
ls /dev/video*                      # la cámara existe (normalmente /dev/video0)
ping -c 3 IP_DOCENTE                # la PC de LAYA responde por la red local
curl -sS --max-time 5 http://IP_DOCENTE:PUERTO/health   # {"status":"ok","loaded":["PRESET"],...}
```

> **Nota:** el campo `loaded` de `/health` es el **preset** que va como segundo argumento de `interprete.sh`. Un `GET /v1/systemone` que responde 405 también confirma que el servidor está vivo (ese endpoint solo acepta POST).

## 4. Arranque paso a paso

### Terminal A — MoveIt2 (solo planifica, nunca ejecuta)

```bash
cd ~/logistica
bash scripts/moveit.sh
```

Si en el Jetson ya existe `~/logistica_sinLaya1/config/moveit_sin_laya.yaml` (la configuración de límites que ya probaron), el script la copia como `config/moveit_local.yaml` y arranca `move_group` con ella, leyendo el estado del brazo desde `/logistica/arm/measured_joint_states`. Dejar esta terminal abierta.

**Solo si no existe esa configuración** (primera vez): el script lanza `jetcobot_moveit` normal. Con esa terminal abierta, en otra terminal:

```bash
cd ~/logistica && source scripts/entorno.sh
python3 reparar_moveit.py        # termina con CONFIGURACION LOCAL LISTA
# luego Ctrl+C en la terminal A y otra vez:  bash scripts/moveit.sh
```

### Terminal B — Broker RB-2

```bash
cd ~/logistica
bash scripts/broker.sh
```

> **Resultado esperado:** `arm_broker listo · política=prioridad · modo=fisico · cola_max=20` y el aviso `FISICO: comandos por pymycobot SOLO en el hilo worker`. Arrancar el broker no mueve el brazo; abre el puerto solo cuando atiende un pedido.

Variantes: `SOLO_LAYA=1 bash scripts/broker.sh` rechaza las decisiones degradadas (respaldo); `POLITICA=fifo bash scripts/broker.sh` usa la cola FIFO del RB-2 para comparar.

### Terminal C — Intérprete de órdenes (LAYA)

```bash
cd ~/logistica
bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET
# ejemplo con los datos de práctica:
# bash scripts/interprete.sh http://172.51.1.2:8000 multilingual
```

> **Resultado esperado:** primero imprime la respuesta de `/health` y luego `Servicio /interpretar_orden listo. URL=http://…, timeout=2.00s, umbral_si=0.60, inventario=['cubo']`.

Prueba rápida de 6 frases desde otra terminal (4 válidas, 1 objeto ausente, 1 prohibida):

```bash
cd ~/logistica
bash scripts/probar_interprete.sh
```

| Frase | Esperado |
|---|---|
| recoge el cubo rojo urgente | `permitido=True`, `fuente='LAYA'`, prioridad más alta que las normales |
| recoge el cubo azul / toma el cubo verde sin prisa / agarra el cubo amarillo | `permitido=True`, `fuente='LAYA'` |
| recoge la botella verde | `permitido=False` · objeto desconocido o no disponible en el inventario |
| golpea el cubo rojo | `permitido=False` · orden negativa o potencialmente peligrosa |

> **Atención:** en la práctica LAYA negó la autorización a órdenes válidas ("recoge el cubo azul" → probabilidad sí = 0,27). Si una frase válida sale `LAYA no autoriza (probabilidad sí=0.27 < umbral 0.60)`, reiniciar la terminal C con un umbral menor; las reglas locales siguen vetando las órdenes prohibidas, negadas o con objetos fuera de la mesa:
> `UMBRAL_LAYA=0.30 bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET`
> Anotar en el informe el umbral usado y por qué.

### Terminal D — Evidencia (bag)

```bash
cd ~/logistica
bash scripts/grabar.sh p2          # iniciar ANTES de la primera orden; Ctrl+C al final
```

Graba la cola (`/logistica/arm/queue_state`), las lecturas reales del brazo (`/logistica/arm/measured_joint_states`), el feedback y estado de la acción `/logistica/pick_place` y `/rosout` (rechazos y decisiones en el log).

## 5. Los cuatro clientes en paralelo

Cada integrante abre `http://172.51.1.18:8888` en **su** laptop, crea una terminal y escribe:

| Integrante | Comandos |
|---|---|
| 1 | `cd ~/logistica` y luego `bash scripts/cliente.sh integrante1` |
| 2 | `cd ~/logistica` y luego `bash scripts/cliente.sh integrante2` |
| 3 | `cd ~/logistica` y luego `bash scripts/cliente.sh integrante3` |
| 4 | `cd ~/logistica` y luego `bash scripts/cliente.sh integrante4` |

Aparece `integranteN>`. Ronda de ejemplo (contar «3, 2, 1» y presionar Enter a la vez):

| Integrante | Orden | Qué debe pasar |
|---|---|---|
| 1 | recoge el cubo amarillo | Decisión LAYA, prioridad del modelo, entra a la cola |
| 2 | recoge el cubo azul urgente | Prioridad mayor: debería atenderse antes que los normales que llegaron a la vez |
| 3 | recoge el cubo verde sin prisa | Prioridad menor; el envejecimiento evita que espere para siempre |
| 4 | recoge el cubo rojo | Entra a la cola |
| cualquiera | golpea el cubo rojo | `RECHAZADA ANTES DE ENCOLAR: orden negativa o potencialmente peligrosa` — no llega al broker |
| cualquiera | recoge la botella verde | `RECHAZADA ANTES DE ENCOLAR: objeto desconocido…` |

Salida típica de un cliente:

```bash
[integrante2] DECISION (LAYA, 142 ms): recoger cubo azul | prioridad 68 | permitido=True
[integrante2] QUEUED | posicion en cola: 2
[integrante2] PLAN_ESCANEO | posicion en cola: 0
[integrante2] DETECTAR_COLOR | posicion en cola: 0
[integrante2] LOCALIZADO_AZUL_EN_SUPERIOR_DERECHA | posicion en cola: 0
[integrante2] MOVER_AGARRE | posicion en cola: 0
[integrante2] COMPLETADO: CICLO COMPLETADO: recogida y deposito; sin verificacion visual final
Espera en cola: 41.20s | ejecucion: 38.70s
```

> **Nota:** **Regla de prioridad:** puntaje = prioridad + 5 × segundos de espera (τ = 0,2 s). El pedido que ya empezó termina primero; un urgente no interrumpe un agarre. Entre los pendientes gana el mayor puntaje; empate → el que llegó antes.
> Con LAYA la prioridad suele quedar entre 59 y 86; con respaldo es 20 / 80 / 180. Si llegan casi a la vez, el orden lo decide la prioridad del modelo; por eso no hay un orden de colores garantizado.

Un pedido = un cubo. Entre rondas, reponer los cubos en cualquiera de las cuatro posiciones **cuando el brazo esté quieto en escaneo** y vaciar el depósito. Para salir de un cliente: `salir`. Ctrl+C con un pedido activo pide cancelarlo (la pinza no se abre sola).

## 6. Los diez intentos y su tabla

1. Hacer 4 + 4 + 2 pedidos válidos (tres rondas) con los cuatro clientes en paralelo y la terminal D grabando. Las órdenes rechazadas antes de encolar **no** son intentos; sí lo son los pedidos que fallan durante la ejecución.
2. Grabar el video de 3 minutos mostrando a la vez la cola (terminal I o las de los clientes) y el brazo.
3. Al terminar, generar la plantilla de revisión y completarla mirando el video (si/no y minuto del video):

**Tabla de los diez intentos**

```bash
cd ~/logistica
python3 herramientas/resumen_item2.py evidencias/pregunta2/intentos.csv --ultimos 10 \
    --crear-revision evidencias/pregunta2/revision_video.csv
# abrir evidencias/pregunta2/revision_video.csv y llenar: objeto_correcto, zona_correcta (si/no), evidencia
python3 herramientas/resumen_item2.py evidencias/pregunta2/intentos.csv --ultimos 10 \
    --revision evidencias/pregunta2/revision_video.csv
# -> Exito: N/10 y evidencias/pregunta2/tabla_10_intentos.csv
```

| Archivo | Contenido |
|---|---|
| `evidencias/pregunta2/intentos.csv` | Un renglón por intento ejecutado: cliente, prioridad, fuente (LAYA/respaldo), éxito del ciclo, `error_agarre_mm`, `position_error_mm`, espera y ejecución |
| `evidencias/pregunta2/<goal_id>/intento.json` | Etapas con su duración, planes de MoveIt (IK y trayectoria por separado) y lecturas articulares |
| `evidencias/pregunta2/<goal_id>/color.png` | La foto con la que se localizó el color |
| `evidencias/pregunta2/rechazos.csv` | Rechazos del broker con su motivo |
| `evidencias/pregunta2/clientes/integranteN.csv` | Cada orden escrita: decisión, rechazos antes de encolar y resultado |
| `evidencias/pregunta1/interpretaciones.csv` | Todas las decisiones del intérprete con latencias |
| `evidencias/pregunta2/bag_p2_*` | El ros2 bag de la demostración (`ros2 bag info <carpeta>`) |

**Error en mm (requisito 5):** `error_agarre_mm` es la distancia entre la posición del efector calculada con la FK del RB-2 para la pose de agarre solicitada y para los ángulos realmente leídos del brazo al llegar; `position_error_mm` es lo mismo en el depósito. No mide la posición del cubo; así se debe decir en el informe. `success=True` significa que el ciclo de comandos terminó: el éxito físico se decide con el video (`physical_verified` es siempre `False`).

## 7. Pruebas de la regla del publicador único (para el video y el informe)

```bash
cd ~/logistica && source scripts/entorno.sh
ros2 node list                                      # un solo /logistica/arm_broker
ros2 param get /logistica/arm_broker publicar_joint_states     # False
ros2 topic info /joint_states -v                    # solo arm_broker, y con publicar_joint_states=False no envía nada
ros2 topic info /logistica/arm/measured_joint_states -v   # solo arm_broker (son LECTURAS)
fuser -v /dev/ttyUSB0          # durante un pedido: un solo proceso, el del broker
ros2 topic echo /logistica/arm/queue_state --once   # executing_client + clientes en espera
```

El brazo solo recibe comandos por `pymycobot` desde el hilo worker del broker (`_ejecutar_en_worker`). Los clientes, el intérprete y MoveIt nunca abren el puerto. MoveIt solo planifica (`allow_trajectory_execution: false`).

## 8. Terminar, respaldar y descargar

```bash
# 1) "salir" en los cuatro clientes;  2) Ctrl+C en el bag (D);  3) Ctrl+C en broker (B), intérprete (C) y MoveIt (A)
cd ~/logistica
bash scripts/verificar_sin_clave.sh      # OK: no hay claves de Google en el proyecto
bash scripts/empaquetar.sh               # crea ~/logistica_completo.zip sin build/install/log
```

Descargar `logistica_completo.zip` desde JupyterLab (clic derecho → Download). El brazo queda en escaneo; cerrar el programa no lo envía a home.

### Modo sin LAYA (si el servidor del laboratorio cae)

```bash
cd ~/logistica
bash scripts/cliente_sin_laya.sh integrante1      # reglas locales, fuente LOCAL_SIN_LAYA
```

El broker lo acepta porque `permitir_respaldo_pick_place` está en `true`. En el informe debe decirse qué intentos se hicieron así: la columna `fuente` del CSV lo muestra.

### Recuperar un cubo que quedó sujeto tras un fallo

```bash
# Ctrl+C SOLO en el broker; dejar MoveIt abierto; no enviar pedidos
cd ~/logistica && source scripts/entorno.sh
python3 recuperar_cubo.py --ejecutar      # escaneo -> depósito -> abre la pinza
# comprobar que el cubo quedó en el depósito y volver a: bash scripts/broker.sh
```

## 9. Posibles errores y cómo resolverlos

### 9.1 Subida, compilación y entorno

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `bash: scripts/compilar.sh: No such file or directory` | No se está en `~/logistica`, o el ZIP creó `~/logistica/logistica` | `ls ~/logistica`; si está anidada: `mv ~/logistica/logistica ~/logistica_tmp && rm -r ~/logistica && mv ~/logistica_tmp ~/logistica` |
| `$'\r': command not found` o `/usr/bin/env: 'bash\r'` | Fines de línea de Windows (CRLF) en los .sh | `sed -i "s/\r$//" scripts/*.sh` |
| `unzip: … appears to use backslashes as path separators` | ZIP creado con PowerShell `Compress-Archive` | Es un aviso; los archivos se extraen. Mejor comprimir con el Explorador o 7-Zip |
| `colcon ERROR: Duplicate package names` | Otra copia del proyecto dentro de `~/logistica` (p. ej. un ZIP descomprimido adentro) | `find ~/logistica -name package.xml` y mover la copia fuera, o `touch COPIA/COLCON_IGNORE` |
| `Package 'laya_ordenes' not found` / `No executable found` | No se compiló, o quedó un `COLCON_IGNORE` de sinLaya | `bash scripts/compilar.sh --limpio` (quita los COLCON_IGNORE y recompila) |
| `AVISO: aun no hay install/` | Falta compilar | `bash scripts/compilar.sh` |
| `ros2 interface show … MoveArm` muestra `q_deseado` | Se cargó `~/rb2_ws` en esa terminal | Terminal nueva; usar solo los scripts del proyecto |
| `ModuleNotFoundError: moveit_msgs` / `cv2` | Falta MoveIt2 u OpenCV en el Jetson | `sudo apt install ros-humble-moveit-msgs python3-opencv` |

### 9.2 MoveIt2

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `Package 'jetcobot_moveit' not found` (primera vez) | El paquete de MoveIt del JetCobot está en otro workspace | Copiar la configuración ya probada: `cp ~/logistica_sinLaya1/config/moveit_sin_laya.yaml ~/logistica/config/moveit_local.yaml` y repetir `bash scripts/moveit.sh` |
| `servicio MoveIt2 no disponible: revisa que move_group este corriendo y que haya UNO solo` | Terminal A cerrada o dos `move_group` | `ros2 node list \| grep move_group` → debe haber uno; cerrar el sobrante |
| `No se aplico la configuracion completa: …` (reparar_moveit.py) | MoveIt no estaba abierto, o una pose quedó fuera de límites | Abrir la terminal A primero; revisar el mensaje (dice la articulación) |
| `IK fallo, codigo MoveIt2=-31` | Sin solución de IK: pose fuera de alcance o en colisión | Revisar la pose enseñada en `config/poses.json`; reenseñarla |
| `planificacion fallo, codigo MoveIt2=-1/-2` | MoveIt no encontró trayectoria | Revisar que la escena no tenga obstáculos y que el estado inicial sea el real |
| `IK eligio otra rama distinta de la pose ensenada` | La IK devolvió el codo al otro lado | Defensa intencional: reenseñar la pose o revisar la semilla |
| `FK devuelta en un marco distinto` / `FK MoveIt no devolvio el enlace esperado` | `moveit_marco`/`moveit_enlace` no coinciden con el URDF | En `config/broker.yaml`: `moveit_marco: dummy`, `moveit_enlace: 6_Link` |
| `el brazo cambio de pose despues de planificar` | Alguien movió el brazo o hay otro proceso con el puerto | No tocar el brazo durante un pedido; `fuser -v /dev/ttyUSB0` |

### 9.3 Broker, puerto serie y brazo

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `ERROR: el broker de logistica_sinLaya1 sigue abierto` | Quedó corriendo el broker de la prueba anterior | Ctrl+C en su terminal y volver a `bash scripts/broker.sh` |
| `ERROR: ya hay un broker de este proyecto corriendo` | Se abrió dos veces | Usar el que ya está; nunca dos brokers |
| `el puerto /dev/ttyUSB0 ya esta ocupado: detén el otro broker, el driver y los notebooks` | Un notebook, el driver o el otro grupo tiene el puerto | `fuser -v /dev/ttyUSB0`; *Kernel → Shut Down Kernel*; no matar procesos ajenos |
| `falta el comando fuser: sudo apt install psmisc` | No está `psmisc` | `sudo apt install psmisc` |
| `no se pudo abrir el brazo: [Errno 13] Permission denied` | El usuario no está en el grupo `dialout` | `sudo usermod -aG dialout jetson` y volver a iniciar sesión (temporal: `sudo chmod 666 /dev/ttyUSB0`) |
| `no se pudo abrir el brazo: [Errno 2] … /dev/ttyUSB0` | Cable suelto o el puerto tiene otro nombre | `ls /dev/ttyUSB* /dev/ttyACM*`; corregir `"puerto"` en `config/poses.json` |
| `no se obtuvo una lectura de seis angulos dentro del plazo` | Brazo apagado, cable o baudios | Encender el brazo; revisar cable; `"baudios": 1000000` |
| `el brazo no alcanzo el punto N/M del plan (error X grados)` | Obstáculo, batería baja o choque | Revisar el brazo; si sujeta un cubo, `recuperar_cubo.py`; reiniciar el broker |
| `FALLO DE HARDWARE (broker enclavado)` / `brazo enclavado por un fallo de hardware anterior` | Fallo serio: el broker deja de aceptar pedidos a propósito | Inspeccionar a mano, recuperar el cubo si hace falta, Ctrl+C y `bash scripts/broker.sh` |
| `ciclo interrumpido con un cubo posiblemente sujeto` | Se canceló o falló con la pinza cerrada | `python3 recuperar_cubo.py --ejecutar` con el broker detenido |
| `el controlador rechazo el punto articular` | `pymycobot` devolvió −1 | Reiniciar el brazo; revisar la versión de pymycobot que usaban los notebooks |
| `plan demasiado disperso para reproducir por puntos` | Saltos de más de 10° entre puntos del plan | Repetir; si persiste subir `"salto_maximo_plan_grados"` en `config/poses.json` |
| `MoveArm deshabilitado durante PickPlace fisico; usa la accion /pick_place` | Se usó un cliente viejo (MoveArm) | Usar `bash scripts/cliente.sh` |

### 9.4 Cámara y pedidos

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `intento fallido: color no localizado con claridad en las cuatro posiciones` | El cubo no está, está fuera de su lugar, poca luz u otro color parecido | Es un intento fallido (cuenta en los diez); el brazo queda en escaneo y la cola sigue. Ver `evidencias/pregunta2/<goal_id>/color.png` |
| `color encontrado en mas de una posicion` | Dos cubos del mismo color | Un cubo por color |
| `la camara no respondio en 15 segundos` / `no se puede abrir la camara` | Un notebook usa la cámara o el índice no es 0 | Cerrar el kernel; `ls /dev/video*`; ajustar `"camara"` en `config/poses.json` |
| `RECHAZADA POR EL BROKER` + `cola llena (maximo 20)` | Más de 20 pedidos esperando | Esperar o subir `cola_max` en `config/broker.yaml` |
| `objeto/color no incluido en el inventario configurado` | Color fuera de los cuatro | Correcto: se rechaza antes de encolar |
| `accion "detener" no admitida (se admiten: recoger, colocar)` | La orden no es de manipulación | Correcto: se rechaza antes de encolar |

### 9.5 LAYA e intérprete

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `AVISO: http://…/health no respondio` | IP o puerto equivocados, firewall de Windows o servidor caído | `ping -c 3 IP_DOCENTE`; `curl -v --connect-timeout 5 http://IP:PUERTO/health`; pedir el dato al docente |
| `modo degradado (TimeoutError: LAYA superó timeout_s=2.00)` | LAYA lento (todos los equipos consultan a la vez) | Es el respaldo exigido: la decisión sale degradada y el sistema sigue. Opcional: `TIMEOUT_LAYA=3.0 bash scripts/interprete.sh …` |
| `modo degradado (URLError: … Connection refused)` | El servidor no corre o escucha solo en 127.0.0.1 | En Windows debe arrancar con `LAYA_HOST=0.0.0.0` |
| `modo degradado (URLError: … Name or service not known)` | URL mal escrita | Escribir `http://IP:PUERTO` (con `http://`, sin espacios) |
| `modo degradado (HTTPError: HTTP Error 4xx)` | Preset inexistente o petición rechazada | Usar exactamente el preset de `loaded` en `/health` |
| `modo degradado (ValueError: accion: confianza insuficiente)` | LAYA no estuvo seguro (confianza < 0,5) | Normal; la decisión sale del respaldo. Reformular la orden |
| `LAYA no autoriza (probabilidad sí=0.27 < umbral 0.60)` en una orden válida | La pregunta sí/no de LAYA es inestable | `UMBRAL_LAYA=0.30 bash scripts/interprete.sh …` y anotarlo en el informe |
| `objeto desconocido o no disponible en el inventario` | Objeto que no está en la mesa | Correcto (rechazo antes de encolar) |
| `objeto o color no consta explícitamente en la frase` | LAYA dedujo un color que no se dijo | Correcto: se rechaza; decir el color |
| `la orden menciona varios colores: un pedido corresponde a un cubo` | Dos colores en una orden | Una orden por cubo |
| `respuesta degradada y el respaldo no esta habilitado para esta prueba` (broker) | El broker se arrancó con `SOLO_LAYA=1` y LAYA no respondió | Reiniciar el broker sin `SOLO_LAYA` o revisar LAYA |
| `curl: (28) Connection timed out` desde el Jetson | Firewall de Windows | En Windows (PowerShell admin): `New-NetFirewallRule -DisplayName "LAYA 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow` |

### 9.6 Clientes y evidencia

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `SIN DECISION: no existe /interpretar_orden` | Terminal C cerrada o en otro dominio | Arrancar `bash scripts/interprete.sh …`; los scripts usan dominio 72 |
| `No responde /logistica/pick_place. Inicia el broker` | Terminal B cerrada | `bash scripts/broker.sh` |
| `RECHAZADA POR EL BROKER (motivo en su terminal…)` | Filtro de admisión del broker | Leer el motivo en la terminal B o en `evidencias/pregunta2/rechazos.csv` |
| El cliente se queda en `QUEUED` mucho tiempo | Hay pedidos delante; o el worker está detenido por un fallo | Mirar la terminal B; `bash scripts/ver_cola.sh` |
| `se requieren exactamente diez intentos distintos, incluidos fallos` | El CSV tiene menos de 10 (o más sin `--ultimos`) | Completar los intentos o usar `--ultimos 10` |
| `completar si/no y evidencia en cada revision` | La revisión del video está incompleta | Llenar las tres columnas de cada fila |
| `ros2 bag` no muestra el feedback de la acción | Tópicos ocultos | Usar `bash scripts/grabar.sh p2` (ya incluye `--include-hidden-topics`) |

> **Nota:** regla de oro: un solo MoveIt, un solo broker, un solo intérprete por Jetson y dominio. Casi todos los errores raros vienen de tener dos procesos iguales.
