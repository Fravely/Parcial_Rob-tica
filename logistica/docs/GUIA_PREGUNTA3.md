# Guía paso a paso — Pregunta 3: De la voz al movimiento

**Equipo:** JetCobot `172.51.9.15` · ROS 2 Humble · `ROS_DOMAIN_ID=52` · LAYA (práctica) `http://172.51.1.2:8000`
**Regla de oro:** la IP, el puerto y el preset de LAYA del día del examen los da el docente. Reemplacen los de práctica.

La pregunta no pide construir nada aguas abajo: se **antepone** una etapa (voz → texto) a lo que ya funciona
(`/interpretar_orden` → cola del broker → brazo). Todo el código nuevo está en:

| Archivo | Para qué |
|---|---|
| `src/laya_ordenes/laya_ordenes/transcriptor_voz.py` | **Nodo `transcriptor_voz` (Parte A)**: micrófono/WAV → Google AI Studio → texto → `/interpretar_orden` → broker. Tiempo límite propio, modo texto, evidencias y tiempos (Parte C). |
| `src/laya_ordenes/laya_ordenes/cadena.py` | Cliente común: servicio `/interpretar_orden` + acción `/pick_place` del broker, con marcas de tiempo. |
| `src/laya_ordenes/laya_ordenes/interfaz_ordenes.py` | Interfaz web para escribir el *prompt* desde la PC de cada integrante (sirve también para la P2). |
| `herramientas/desglose_tiempos.py` | Parte C: tabla y figura del desglose de tiempos + tabla de las 5 órdenes (Parte B). |
| `herramientas/parche_respaldo.py` | Opcional, recomendado: corrige 5 fallas del clasificador de respaldo (ver §1.7). |

---

## 0. Qué hay que entregar (checklist)

- [ ] Código del nodo `transcriptor_voz` en el repositorio (sin la clave).
- [ ] Archivos de audio `.wav` con su transcripción `.json` (carpeta `evidencias/pregunta3/`).
- [ ] Tabla de las **5 órdenes dictadas**: lo que se dijo / lo que transcribió / decisión del modelo / lo que hizo el brazo / ¿correcta?
- [ ] **Desglose de tiempos** en tabla **y** figura, con la respuesta numérica: etapa dominante y qué se sacrificaría para reducir el tiempo a la mitad.
- [ ] **Demostración del modo texto con internet desconectado** (video + fila `modo=texto` en el CSV + aviso en el log).
- [ ] Predicciones escritas **antes** de medir (el examen califica la diferencia entre predicho y medido).
- [ ] `ros2 bag` de la demostración.

---

## 1. Preparación (hacerla ANTES del examen)

### 1.1 Copiar los archivos al Jetson

Abran JupyterLab (`http://172.51.9.15:8888`) y suban los archivos a **la carpeta del workspace que de verdad usan**.
La versión con la acción `PickPlace` (agarre con pinza) es la de `~/logistica_prueba/logistica1`; si usan otra,
cambien la ruta en todos los comandos. En esta guía se usa la variable `WS`:

```bash
export WS=~/logistica_prueba/logistica1      # ← CAMBIAR si su workspace es otro (p. ej. ~/logistica)
ls $WS/src                                     # deben verse arm_broker, arm_broker_interfaces, laya_ordenes...
```

Destinos:

```
$WS/src/laya_ordenes/laya_ordenes/cadena.py
$WS/src/laya_ordenes/laya_ordenes/interfaz_ordenes.py
$WS/src/laya_ordenes/laya_ordenes/transcriptor_voz.py
$WS/herramientas/desglose_tiempos.py
$WS/herramientas/parche_respaldo.py
```

### 1.2 Registrar los dos nodos nuevos en `setup.py`  ← **AQUÍ SE MODIFICA**

Archivo: `$WS/src/laya_ordenes/setup.py`. Dentro de `entry_points` → `console_scripts`, agreguen **dos líneas**:

```python
    entry_points={
        'console_scripts': [
            'interprete_ordenes = laya_ordenes.node:main',
            'orden_a_broker = laya_ordenes.orden_a_broker:main',
            'interfaz_ordenes = laya_ordenes.interfaz_ordenes:main',     # ← NUEVA
            'transcriptor_voz = laya_ordenes.transcriptor_voz:main',     # ← NUEVA
        ],
    },
```

Y en `$WS/src/laya_ordenes/package.xml`, debajo de `<exec_depend>rclpy</exec_depend>`:

```xml
  <exec_depend>std_msgs</exec_depend>
```

### 1.3 Compilar

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
cd $WS
colcon build --symlink-install --packages-select laya_ordenes
source install/setup.bash
ros2 pkg executables laya_ordenes
```

Debe listar: `interfaz_ordenes`, `interprete_ordenes`, `orden_a_broker`, `transcriptor_voz`.
Comprueben también que existe la acción del broker:

```bash
ros2 interface show arm_broker_interfaces/action/PickPlace
```

> Si `PickPlace` no existe, están en el workspace equivocado (el de `~/logistica` solo tiene `MoveArm`).
> El transcriptor igual funcionará, pero solo interpretará; no podrá encolar el agarre.

### 1.4 Micrófono

```bash
arecord -l                      # lista tarjetas: anoten "card X ... device Y" del micrófono USB
arecord -d 3 -f S16_LE -r 16000 -c 1 prueba.wav && aplay prueba.wav
```

Si el micrófono es la tarjeta 2, dispositivo 0, usen luego `-p dispositivo_alsa:=plughw:2,0`.
Si `arecord` no existe: `sudo apt install alsa-utils`.
**Si el Jetson no tiene micrófono**, consigan uno USB (o un audífono con micrófono USB). Como respaldo, se puede grabar
en otra PC un `.wav` y procesarlo con `-p fuente_audio:=archivo` (ver §3.3), pero el dictado en vivo es lo que se califica.

### 1.5 Clave de Google AI Studio (sin publicarla)

1. Créenla en <https://aistudio.google.com/apikey>.
2. Guárdenla **fuera del repositorio**, en un archivo que solo lee su usuario:

```bash
nano ~/.clave_gemini          # escribir UNA línea:  export GEMINI_API_KEY="AIza...."
chmod 600 ~/.clave_gemini
source ~/.clave_gemini         # en CADA terminal donde corra el transcriptor
python3 -c "import os; print('CLAVE OK' if os.getenv('GEMINI_API_KEY') else 'FALTA CLAVE')"
```

3. Antes de cada `git push`, verifiquen que no se coló:

```bash
cd $WS && git grep -n "AIza" || echo "OK: no hay claves en el repo"
```

El nodo **nunca** imprime la clave ni la escribe en CSV/JSON.

### 1.6 Prueba rápida de transcripción (sin brazo)

```bash
source /opt/ros/humble/setup.bash && export ROS_DOMAIN_ID=52
cd $WS && source install/setup.bash && source ~/.clave_gemini
ros2 run laya_ordenes transcriptor_voz --ros-args -p fuente_audio:=archivo \
  -p archivos_audio:="['$HOME/prueba.wav']" -p dir_evidencias:=$WS/evidencias/pregunta3_pruebas
```

Debe imprimir `📝 Texto (voz): «…»`. Si `/interpretar_orden` está corriendo, también imprimirá la decisión.

Modelo por defecto: `gemini-3.5-flash-lite` (rápido; si devuelve vacío prueba `gemini-3.6-flash`).
Se pueden cambiar con `-p modelo_gemini:=...` y `-p modelo_gemini_respaldo:=...`.
Se usa `generateContent` con el audio en línea: **un solo viaje a la nube**. (El script anterior
`grabar_y_transcribir.py` subía primero el archivo y luego pedía la transcripción con `gemini-3.5-transcribe`:
dos viajes, y ese modelo tiene reportes públicos de devolver texto vacío.)

### 1.7 (Recomendado) Corregir el clasificador de respaldo

En las 50 frases de práctica encontramos que **"fuerza el brazo para recoger la botella verde" salió PERMITIDA**
(la regla busca `forz…` y no `fuerz…`). El docente dictará al menos una orden prohibida: conviene cerrar ese hueco.

```bash
cd $WS
python3 herramientas/parche_respaldo.py src/laya_ordenes/laya_ordenes/logic.py
python3 -m unittest discover -s tests -v            # deben pasar las 9 pruebas
colcon build --symlink-install --packages-select laya_ordenes
```

Efecto medido en las 50 frases de práctica (respaldo): exactitud 4 campos **30/50 → 44/50**, campo permitido **40/50 → 50/50**,
0 falsos permitidos. Ojo: medido sobre el mismo conjunto con el que se diseñó; validar con las frases del docente.

---

## 2. Día del examen: terminales

Abran **5 terminales** en JupyterLab. En **todas** ejecuten primero:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=52
export WS=~/logistica_prueba/logistica1
cd $WS && source install/setup.bash
```

**Terminal A — intérprete (P1).** Con los datos que dicte el docente. El inventario debe ser **exactamente lo que está sobre la mesa**
(si dejan `botella` en la lista y no hay botella, una orden de "botella" saldría permitida):

```bash
ros2 run laya_ordenes interprete_ordenes --ros-args -r __node:=interprete_ordenes \
  -p url_laya:=http://IP_DOCENTE:PUERTO -p modelo_laya:=PRESET_DOCENTE -p timeout_s:=2.0 \
  -p objetos_disponibles:="['cubo']" -p colores_disponibles:="['rojo','azul','verde','amarillo']" \
  -p registro_csv:=$WS/evidencias/pregunta3/interpretaciones_p3.csv
```

**Terminal B — broker (P2).** El mismo comando con el que ya les funcionó el agarre físico, pero con
`politica:=prioridad` (la prioridad que decide el modelo debe influir en el orden):

```bash
ros2 run arm_broker broker --ros-args \
  -p politica:=prioridad -p tau_envejecimiento_s:=8.0 \
  -p publicar_joint_states:=false -p habilitar_movimiento_fisico:=true \
  -p habilitar_recogida_fisica:=true -p accionar_pinza_recogida:=true \
  -p permitir_respaldo_pick_place:=true \
  -p "inventario_pick_place:=['cubo:amarillo','cubo:azul','cubo:verde','cubo:rojo']" \
  -p puerto_robot:=/dev/ttyUSB0 -p baud_robot:=1000000 -p velocidad_robot:=15 \
  -p timeout_robot_s:=30.0 -p paso_fisico_max_rad:=0.15 -p "archivo_rechazos:=''"
```

**Terminal C — bag (evidencia).** Iniciar ANTES de la primera orden y detener con Ctrl+C al final:

```bash
mkdir -p $WS/evidencias/pregunta3
ros2 bag record --include-hidden-topics -o $WS/evidencias/pregunta3/bag_p3_$(date +%H%M) \
  /voz/transcripcion /voz/estado /arm/queue_state /interfaz/ordenes \
  /pick_place/_action/feedback /pick_place/_action/status /rosout
```

**Terminal D — transcriptor de voz (P3):**

```bash
source ~/.clave_gemini
ros2 run laya_ordenes transcriptor_voz --ros-args \
  -p enviar_al_broker:=true -p client_id:=voz \
  -p timeout_transcripcion_s:=6.0 \
  -p dispositivo_alsa:=plughw:2,0 \
  -p dir_evidencias:=$WS/evidencias/pregunta3
```

(quiten `dispositivo_alsa` si el micrófono es el predeterminado). Por defecto `enviar_al_broker` es `false`
(**modo seguro**: interpreta pero no mueve). Para la demostración debe ir en `true`.

**Terminal E — interfaz web (opcional, útil para la P2 y como "modo texto" visible):**

```bash
ros2 run laya_ordenes interfaz_ordenes --ros-args -p puerto_web:=8090 \
  -p registro_csv:=$WS/evidencias/interfaz/ordenes_interfaz.csv
```

Cada integrante abre en su PC `http://172.51.9.15:8090`, escribe su nombre y la orden, y pulsa **Enviar orden**.
Ver §6.

---

## 3. Parte A — Transcripción

### 3.1 Cómo se usa el transcriptor (Terminal D)

```
[ENTER]=grabar · t=escribir orden · q=salir >        ← ENTER para empezar a grabar
  🎙️  GRABANDO… presiona ENTER apenas termine de hablar el docente.
  ☁️  Transcribiendo con Google AI Studio…
  📝 Texto (voz): «recoge el cubo rojo urgente»
  🧠 Decisión: recoger / cubo / rojo · prioridad=68 · permitido=True · LAYA · 142 ms
  📦 Enviada al broker; sigue su avance aquí. Puedes dictar la siguiente.
     ↳ broker [a1b2c3d4] en_cola QUEUED (posición 1)
     ↳ broker [a1b2c3d4] ejecutando POSTURA_OBSERVACION
  ⏱️  Orden 3: voz → movimiento = 2875.4 ms
```

Un integrante maneja el teclado: **ENTER** cuando el docente empieza, **ENTER** apenas termina.
El nodo detecta en el audio el silencio final y lo descuenta, para que el "fin del habla" sea el real y no el del ENTER.

### 3.2 Los tres requisitos de la Parte A y dónde se ven

| Requisito | Cómo lo cumple el nodo | Evidencia |
|---|---|---|
| Clave en variable de entorno | Lee `GEMINI_API_KEY` (o `GOOGLE_API_KEY`); jamás la imprime. | `git grep -n AIza` vacío; código. |
| Tiempo límite propio → modo texto | `timeout_transcripcion_s` (6 s por defecto). Si vence, si no hay internet o si no hay clave: `WARN MODO TEXTO POR TECLADO — motivo`, publica `MODO_TEXTO: motivo` en `/voz/estado` y pide la orden por teclado. | Log, bag (`/voz/estado`), columna `modo=texto` y `motivo_modo_texto` en `voz_cadena.csv`. |
| Guardar transcripción junto al audio | `orden_NN_fecha.wav` + `orden_NN_fecha.json` (texto, modelo, ms) + fila en `voz_cadena.csv`; además publica `/voz/transcripcion`. | Carpeta `evidencias/pregunta3/`. |

### 3.3 Variante con archivo de audio (para pruebas)

```bash
ros2 run laya_ordenes transcriptor_voz --ros-args -p fuente_audio:=archivo \
  -p archivos_audio:="['/home/jetson/o1.wav','/home/jetson/o2.wav']" -p enviar_al_broker:=false
```

### 3.4 Demostración del modo texto **con internet desconectado**

Se necesita cortar internet **sin cortar la red del laboratorio** (LAYA está en la LAN y debe seguir respondiendo:
"la decisión y el movimiento no dependen de internet"). Opción recomendada: bloquear solo Google en el Jetson.

```bash
# 1) PREDICCIÓN escrita antes: "el nodo pasará a modo texto en < 1 s y el brazo igual se moverá"
# 2) Cortar el acceso a Google (reversible):
echo "0.0.0.0 generativelanguage.googleapis.com" | sudo tee -a /etc/hosts
curl -sS --max-time 5 https://generativelanguage.googleapis.com >/dev/null || echo "Google: SIN ACCESO (bien)"
curl -sS --max-time 5 http://IP_DOCENTE:PUERTO/health && echo "  LAYA: sigue respondiendo (bien)"
# 3) En la Terminal D: ENTER, decir una orden, ENTER  -> debe aparecer "MODO TEXTO POR TECLADO — ConnectionError…"
#    escribir la orden (p. ej. "recoge el cubo azul") -> el brazo debe ejecutarla.
# 4) Restaurar internet:
sudo sed -i '/generativelanguage.googleapis.com/d' /etc/hosts
```

Graben en video la terminal D + el brazo durante los pasos 3–4.
Alternativa sin `sudo` (solo para esa terminal): `export https_proxy=http://127.0.0.1:9` antes de lanzar el transcriptor
(`unset https_proxy` para volver). Desconectar el cable/Wi‑Fi del Jetson NO sirve: también cortaría LAYA y JupyterLab.

---

## 4. Parte B — La cadena completa con 5 órdenes dictadas

### 4.1 Antes de que el docente dicte (predicción por escrito)

Copien esta tabla en el informe y llénenla **en cuanto escuchen cada orden y antes de ver el resultado**:

| # | Orden dictada | Resultado esperado (decisión + brazo) |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

Casos especiales que el docente anunció:

- **Objeto que no está sobre la mesa** (p. ej. "recoge la botella verde", "toma la pelota morada"): esperado
  `permitido=False`, motivo *"objeto desconocido o no disponible en el inventario"* → **rechazo antes de encolar**. El brazo NO se mueve. Eso cuenta como **correcta**.
- **Orden no permitida** (p. ej. "golpea el cubo rojo", "fuerza el brazo…"): esperado `accion=peligrosa`, `permitido=False` → rechazo antes de encolar. **Correcta** si se rechaza.
- **Orden válida** (p. ej. "recoge el cubo rojo urgente"): esperado permitido, entra a la cola con la prioridad del modelo y el brazo deposita el cubo correcto en la zona.

### 4.2 Durante

1. Terminal C grabando el bag; cámara/celular grabando brazo + pantalla.
2. Terminal D: ENTER → docente dicta → ENTER. Repetir 5 veces (pueden dictarse seguidas: la cola las ordena).
3. No cierren el transcriptor hasta que todas terminen (con `q` espera a que acaben las que siguen en cola).

### 4.3 Después: completar la tabla

En `evidencias/pregunta3/voz_cadena.csv` (ábranlo en JupyterLab → *Open With → Editor*) completen a mano, para cada fila,
las columnas: `lo_que_se_dijo` (lo que dijo el docente, literal), `lo_que_hizo_el_brazo` (lo observado en el video),
`resultado_esperado` y `correcta` (`sí`/`no`). Luego:

```bash
cd $WS
python3 herramientas/desglose_tiempos.py --csv evidencias/pregunta3/voz_cadena.csv --ordenes 3 4 5 6 7
```

(`--ordenes` = valores de la columna `n` de las 5 órdenes del docente). Genera `tabla_cinco_ordenes.md`,
lista para pegar en el informe.

---

## 5. Parte C — ¿Dónde se va el tiempo?

### 5.1 Qué mide cada etapa (columnas de `voz_cadena.csv`)

| Etapa del enunciado | Columna | Desde → hasta |
|---|---|---|
| Captura del audio | `captura_ms` | fin real del habla (ENTER − silencio final detectado) → WAV cerrado en disco |
| Transcripción en la nube | `transcripcion_ms` | envío del audio a Google → texto recibido |
| Decisión del modelo | `decision_ms` | llamada a `/interpretar_orden` → respuesta (incluye la red hasta Windows; `inferencia_ms` es solo el modelo) |
| (envío al broker) | `envio_a_aceptacion_ms` | goal enviado → broker lo acepta en la cola |
| Espera en la cola del broker | `espera_cola_ms` | aceptado → primer feedback fuera de espera |
| Percepción + IK + planificación | `salida_cola_a_movimiento_ms` | sale de la cola → primer feedback de movimiento |
| **Total** | `voz_a_movimiento_ms` | fin del habla → el brazo inicia el movimiento |

Si el broker publica estados de feedback que contengan `LOCALIZ…`/`PERCEP…`, `:IK`/`CINEMAT…` o `PLAN…`/`TRAYECT…`/`MOVEIT`,
el script separa esas etapas automáticamente (cada estado cuenta en UNA sola etapa). **Si su broker usa posturas calibradas
(sin cámara ni MoveIt2), esas etapas valen prácticamente 0 y así debe decirse en el informe**; no inventen cifras.

**Con el broker de `broker_parte3`:** el primer movimiento es ir a la pose de ESCANEO, y la cámara mira *después*.
Para que percepción, IK y planificación queden dentro del intervalo, definan "el brazo inicia el movimiento" como
el inicio del movimiento hacia el objeto y midan con `--inicio-movimiento MOVER_PREAGARRE`. Reporten también el
valor por defecto (primer movimiento = `MOVER_ESCANEO`) y expliquen en el informe qué definición usaron.

### 5.2 Predicción (escribirla ANTES de medir)

Con lo que ya midieron en la P1 pueden predecir con fundamento:

| Etapa | Predicción | Base |
|---|---|---|
| Captura | 0,3–1,0 s | silencio final + reacción del operador + cierre del WAV |
| Transcripción | 1–3 s | viaje a internet + modelo de audio (medir en 1.6) |
| Decisión (LAYA) | ~0,14 s en calma; más bajo carga | P1: mediana 137 ms, p95 190 ms (en calma) |
| Espera en cola | 0 s si la cola está vacía; ~1 ciclo de agarre por pedido delante | depende de lo encolado |
| Percepción/IK/plan | ≈ 0 s con posturas calibradas | implementación actual |

### 5.3 Medir y graficar

```bash
cd $WS
python3 herramientas/desglose_tiempos.py --csv evidencias/pregunta3/voz_cadena.csv --ordenes 3 4 5 6 7
# con broker_parte3 (movimiento = ir hacia el objeto):
python3 herramientas/desglose_tiempos.py --csv evidencias/pregunta3/voz_cadena.csv --ordenes 3 4 5 6 7 \
  --inicio-movimiento MOVER_PREAGARRE
```

Salidas en `evidencias/pregunta3/`: `desglose_tiempos.csv`, `desglose_tiempos.md` (tabla), `desglose_tiempos.png` (figura).
La consola imprime la etapa dominante y, para cada etapa, cuánto quedaría el total si se eliminara
("¿alcanza la mitad?"). Si falta matplotlib: `pip3 install matplotlib`.

Usen solo órdenes en **modo voz que llegaron a moverse** (las rechazadas no tienen "inicio de movimiento").
Si pocas órdenes del docente se movieron, dicten 3–5 órdenes válidas adicionales para tener datos.

### 5.4 Cómo responder (con SUS números)

> "La etapa dominante fue **[etapa]**, con **[X] ms de [TOTAL] ms (Y %)**. Para reducir el tiempo voz→movimiento a la mitad
> (de [TOTAL] a [TOTAL/2] ms) trabajaríamos sobre **[etapa]**: [acción concreta]. A cambio dejaríamos de obtener **[costo]**."

Opciones típicas y su costo (elijan la que sus números justifiquen):

| Si domina… | Acción | Lo que se pierde |
|---|---|---|
| Transcripción en la nube | Transcripción local en el Jetson (p. ej. Whisper/Vosk pequeño) o streaming (`gemini-3.5-transcribe-live`) | Exactitud (más errores de transcripción), consumo de GPU/RAM en el Jetson; con streaming, dependencia aún mayor de internet |
| Transcripción en la nube | Bajar `timeout_transcripcion_s` | Más caídas a modo texto cuando la red está lenta |
| Captura | Detección automática de fin de habla (VAD) en vez de ENTER | Riesgo de cortar al operador si hace pausas |
| Espera en la cola | Más prioridad a voz / prioridad por envejecimiento más agresiva | Equidad: otros clientes esperan más (inanición) |
| Decisión del modelo | Usar solo el clasificador por palabras clave (sin LAYA) | Exactitud en frases no previstas; robustez semántica |
| Movimiento/planificación | Mayor velocidad del brazo o menos posturas intermedias | Precisión del agarre y seguridad |

---

## 6. La interfaz web del prompt (cómo se usa y dónde se toca)

- **Arranque:** Terminal E (§2). Abran `http://172.51.9.15:8090` desde cada PC.
- **Qué muestra:** la decisión tipada (acción, objeto, color, prioridad, permitido, fuente, ms), la cola del broker en vivo
  (`/arm/queue_state`) y la lista de pedidos de los 4 integrantes con su estado.
- **Regla del publicador único:** la interfaz solo llama al servicio y envía goals; nunca publica al brazo.
- **No permitida:** se rechaza antes de encolar y se muestra el motivo (rojo).
- **Evidencia:** `evidencias/interfaz/ordenes_interfaz.csv` y el tópico `/interfaz/ordenes` (inclúyanlo en el bag de la P2).
- **Dónde modificar:**
  - Puerto, nombre de la acción y zona de depósito → parámetros `puerto_web`, `accion_broker`, `zona`.
  - Los botones de ejemplo (órdenes rápidas) → en `interfaz_ordenes.py`, bloque `<div class="fila chips">` del HTML (`data-f="…"`).
  - Los campos que se copian al goal del broker → `cadena.py`, diccionario `valores` en `enviar_al_broker()`.
  - Los estados de feedback que cuentan como "espera" o "movimiento" → `ESTADOS_ESPERA` y `PREFIJOS_MOVIMIENTO` en `cadena.py`.
- **Si no abre desde otra PC:** en el Jetson `ss -ltnp | grep 8090` (debe escuchar en `0.0.0.0`); si hay firewall, `sudo ufw allow 8090`.

---

## 7. Problemas frecuentes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `arecord no generó audio` | dispositivo equivocado | `arecord -l` y `-p dispositivo_alsa:=plughw:X,Y` |
| `HTTP 400 … API key not valid` | clave mal copiada | regenerar en AI Studio; `source ~/.clave_gemini` |
| `HTTP 429` | cuota gratuita agotada | esperar o usar otra clave del equipo; `-p modelo_gemini:=gemini-3.5-flash-lite` |
| `HTTP 404 … model not found` | nombre de modelo | `-p modelo_gemini:=gemini-3.6-flash` (ver lista en ai.google.dev/gemini-api/docs/models) |
| Transcripción vacía | audio muy bajo o modelo | hablar cerca del micrófono; el nodo prueba el modelo de respaldo |
| `/interpretar_orden no está disponible` | Terminal A caída o otro `ROS_DOMAIN_ID` | revisar Terminal A y `echo $ROS_DOMAIN_ID` |
| `sin acción PickPlace` | workspace equivocado | `source $WS/install/setup.bash` del workspace con `PickPlace` |
| `voz_a_movimiento_ms` vacío | la orden no se movió (rechazada o modo seguro) | normal en rechazos; revisar `enviar_al_broker:=true` |
| No hay figura | falta matplotlib | `pip3 install matplotlib` |
