# Manual de comandos — Pregunta 3: de la voz al movimiento

_Análisis de lo que falta, comandos por terminal, modo texto sin internet, desglose de tiempos y errores posibles_

| Dato | Valor |
|---|---|
| JetCobot (Jetson) | `172.51.1.18` · JupyterLab `http://172.51.1.18:8888` · carpeta `~/logistica` |
| ROS_DOMAIN_ID | `72` (lo fija `scripts/entorno.sh`) |
| Transcripción | Google AI Studio (Gemini) por HTTPS · modelo `gemini-3.5-flash-lite`, respaldo `gemini-3.6-flash` |
| Clave | Solo en la variable `GEMINI_API_KEY`, guardada en `~/.clave_gemini` del Jetson (fuera del repositorio) |
| Decisión | Servicio `/interpretar_orden` → LAYA (PC Windows) o respaldo por palabras clave |
| Cola y brazo | Acción `/logistica/pick_place` del broker RB-2 (el mismo de la Pregunta 2) |
| Evidencias | `evidencias/pregunta3/` (WAV + JSON por orden, `voz_cadena.csv`, desglose, bag) |

> **Cómo usar este manual:** primero lean la sección 1 (qué falta y qué ya quedó resuelto en el código). Luego la Pregunta 3 se ejecuta con las mismas terminales A, B y C de la Pregunta 2 (MoveIt, broker, intérprete) más el transcriptor de voz. Los bloques grises se copian tal cual en una terminal de JupyterLab.

## 1. Análisis: qué falta para completar la Pregunta 3

Se revisó el enunciado contra el código de `logistica` (transcriptor, cadena, intérprete) y contra el broker funcional de `logistica_sinLaya1`. El nodo `transcriptor_voz` ya existía y cubre la Parte A, pero **no podía funcionar con el broker que sí mueve el brazo**: apuntaba a otra acción, otra cola y otro nombre de etapa. Esos problemas se corrigieron en la fusión. Lo que queda pendiente es trabajo en el laboratorio (clave probada, micrófono, internet, mediciones y evidencias), que no se puede hacer desde fuera del Jetson.

### 1.1 Cobertura de cada requisito del enunciado

| Requisito del examen | Cómo lo cumple el proyecto | Estado |
|---|---|---|
| A1. La clave se lee de una variable de entorno; no está en el código ni en el repositorio | `transcriptor_voz` lee `GEMINI_API_KEY` (o `GOOGLE_API_KEY`); nunca la imprime ni la escribe. `scripts/voz.sh` la carga de `~/.clave_gemini`. `.gitignore` excluye `.clave_gemini` y `*.env`. Nuevo `scripts/verificar_sin_clave.sh` detecta claves `AQ.` y `AIza` | Hecho en código · falta crear `~/.clave_gemini` en el Jetson |
| A2. Tiempo límite propio; sin transcripción a tiempo o sin internet → modo texto por teclado, informándolo | Parámetro `timeout_transcripcion_s` (6 s). Timeout, error de red, clave ausente o texto vacío → `WARN MODO TEXTO POR TECLADO — motivo`, mensaje en `/voz/estado` y pide la orden por teclado | Hecho · falta demostrarlo con internet cortado (sección 6) |
| A3. Guardar la transcripción junto con el audio original | Cada orden: `orden_NN_fecha.wav` + `orden_NN_fecha.json` (texto, modelo, ms) + fila en `voz_cadena.csv` + tópico `/voz/transcripcion` | Hecho |
| A. El texto se entrega a `/interpretar_orden` de la P1 | `cadena.py` llama al servicio; solo el intérprete habla con LAYA | Hecho |
| B. Cinco órdenes dictadas, extremo a extremo (incluye objeto ausente y orden no permitida) | No permitido → rechazo antes de encolar con su causa. Permitido → goal `/logistica/pick_place` con la prioridad del modelo | Código listo · falta la demostración y llenar la tabla |
| B. Reportar dicho / transcrito / decisión / lo que hizo el brazo | `voz_cadena.csv` guarda transcripción, decisión y resultado del broker; `desglose_tiempos.py` genera `tabla_cinco_ordenes.md` | Falta completar a mano "lo que se dijo", "lo que hizo el brazo" y "correcta" |
| C. Tiempo desde que se termina de hablar hasta que el brazo inicia el movimiento, por etapas | Marcas de tiempo por etapa en el transcriptor y en el feedback del broker; `desglose_tiempos.py` produce tabla (CSV/MD) y figura (PNG) | Falta medir y responder con números |
| Entregable: demostración del modo texto con internet desconectado | Procedimiento y verificación en la sección 6 | Falta grabarla |

### 1.2 Lo que se corrigió en el código durante la fusión

| Problema encontrado | Consecuencia si no se corregía | Corrección |
|---|---|---|
| El transcriptor enviaba a `/pick_place` y escuchaba `/arm/queue_state`; el broker funcional usa un espacio de nombres propio | Mensaje "La acción del broker no está disponible": la voz nunca llegaba al brazo | Broker bajo `/logistica`; transcriptor, cliente e interfaz usan `/logistica/pick_place` y `/logistica/arm/queue_state` (parámetros `accion_broker`, `topico_cola`) |
| Los paquetes LAYA tenían `COLCON_IGNORE` en `logistica_sinLaya1` | No existían `interprete_ordenes` ni `transcriptor_voz` | `scripts/compilar.sh` compila los 4 paquetes y quita esos marcadores |
| La Parte C medía hasta `MOVER_PREAGARRE` (nombre de otra versión del broker) | Columna `voz_a_movimiento_ms` vacía o medida hasta ir a escaneo (antes de la cámara) | Inicio del movimiento = `MOVER_AGARRE` (el brazo va al cubo después de cámara, IK y plan); configurable |
| Tres escalas de prioridad (local 1–3, LAYA 59–86, respaldo 20–180) con τ = 8 s | Un respaldo aplastaba a LAYA y el envejecimiento no hacía nada | Escala única del modelo; τ = 0,2 s (50 puntos ≈ 10 s de espera) |
| La verificación del examen era `git grep AIza` | Las claves nuevas empiezan con `AQ.`: una clave filtrada no se detectaba | `bash scripts/verificar_sin_clave.sh` busca ambos formatos |
| `reparar_moveit.py` leía `recogida_grados`, que ya no existe en las poses | KeyError al preparar MoveIt en una carpeta nueva | Lee las cuatro `posiciones_recogida` |
| El broker solo admitía la acción `recoger` | "Lleva/deposita el cubo X" (acción `colocar` de LAYA) se rechazaba | Se admiten `recoger` y `colocar` (misma tarea física) |
| Una orden con dos colores pasaba con el primero | Se movía un cubo que quizá no era el pedido | Se rechaza antes de encolar |
| Clasificador de respaldo sin el parche de la práctica | "fuerza el brazo…" salía permitida; colores en femenino fallaban | Parche aplicado (prohibidas, femenino, "para", "mueve", "lleva") |
| `ROS_DOMAIN_ID=52` fijo en herramientas | Riesgo de mandar pedidos al dominio de otro equipo | Cambiado a 72 |
| El umbral de autorización de LAYA era fijo (0,60) | LAYA negó órdenes válidas en la práctica (sí = 0,27) | Parámetro `umbral_autorizacion` (`UMBRAL_LAYA=…`) |

### 1.3 Lo que falta hacer en el laboratorio (en este orden)

| # | Tarea | Comando o acción | Hecho cuando… |
|---|---|---|---|
| 1 | Subir y compilar la carpeta fusionada | `bash scripts/compilar.sh --limpio` (manual P2, sección 2) | `Summary: 4 packages finished` |
| 2 | Guardar la clave fuera del repositorio | Sección 2.1 (`~/.clave_gemini`) | `probar_gemini.sh` dice `OK autenticacion` |
| 3 | **Probar YA la clave nueva `AQ.`** | `bash scripts/probar_gemini.sh` | Responde `OK generateContent`. Hay reportes de claves `AQ.` con `401 ACCESS_TOKEN_TYPE_UNSUPPORTED`: si pasa, generar otra clave antes del examen |
| 4 | Confirmar que el Jetson tiene internet (HTTPS a Google) | `curl -sS -o /dev/null -w "%{http_code}\n" https://generativelanguage.googleapis.com` | Devuelve un código HTTP (404 está bien); un error de conexión significa sin internet |
| 5 | Conectar y probar el micrófono USB en el Jetson | `arecord -l` y grabación de prueba (sección 2.2) | Se oye la voz en `prueba.wav` y `probar_gemini.sh prueba.wav` la transcribe |
| 6 | Tener funcionando la cadena de la P2 con LAYA | Terminales A, B y C (manual P2) | Una orden escrita mueve el brazo |
| 7 | Escribir las predicciones antes de medir | Tabla de la sección 7.2 | Están en el informe con hora |
| 8 | Ensayar 3–5 órdenes de voz válidas | Sección 4 | `voz_a_movimiento_ms` tiene valor |
| 9 | Demostrar el modo texto con internet cortado (video) | Sección 6 | Fila `modo=texto` + motivo `ConnectionError` + el brazo se mueve |
| 10 | Las cinco órdenes del docente y su tabla | Sección 5 | `tabla_cinco_ordenes.md` completa |
| 11 | Desglose de tiempos con figura y respuesta | Sección 7 | `desglose_tiempos.md` y `.png` + párrafo con números |
| 12 | Entregar sin clave | `bash scripts/verificar_sin_clave.sh` y `git push` | `OK: no hay claves…` |

### 1.4 Riesgos que hay que declarar en el informe

- **Transcripción = red + modelo.** Google no informa por separado su tiempo de cálculo; `transcripcion_ms` incluye el viaje por internet.
- **"Inicio del movimiento".** Con este broker el primer movimiento es ir a la pose de escaneo y la cámara mira después. Se mide hasta `MOVER_AGARRE` (el brazo va hacia el cubo) para que percepción, IK y planificación queden dentro del intervalo; se reporta también la otra definición (`--inicio-movimiento MOV`).
- **Objeto ausente.** "Recoge la botella…" se rechaza antes de encolar. Pero si se pide un cubo de un color que fue retirado de la mesa, la orden sí se encola y falla en la cámara (`color no localizado`): el brazo va a escaneo y no agarra nada. Hay que explicarlo así si ocurre.
- **Éxito físico.** `physical_verified` es siempre `False` (no hay verificación visual del depósito): el resultado del brazo se confirma con el video.
- **LAYA inestable en la autorización.** Si se baja el umbral, decir cuál y por qué; las reglas locales siguen vetando órdenes prohibidas, negadas o con objetos ausentes.
- **Respaldo.** Si LAYA no responde en 2 s la decisión sale degradada (`fuente=respaldo`) y el broker la atiende; la columna `fuente` de los CSV lo muestra.
- **Medir con la cola vacía.** Si se dictan órdenes seguidas, la espera en cola (≈ un ciclo de agarre por pedido delante) tapa a todas las demás etapas. Medir la Parte C dictando una orden y esperando a que termine; reportar aparte el caso con cola.

## 2. Preparación (antes del examen)

### 2.1 Clave de Google AI Studio, fuera del repositorio

La clave que crearon (empieza con `AQ.Ab8R…`) **no se escribe en ningún archivo del proyecto**: el examen descuenta puntos si aparece en el repositorio. Se guarda en un archivo del usuario `jetson` que solo él puede leer. Sin que la clave quede en pantalla ni en el historial:

**Guardar y probar la clave**

```bash
read -r -s -p "Pega la clave y presiona ENTER: " K && echo
printf 'export GEMINI_API_KEY="%s"\n' "$K" > ~/.clave_gemini && unset K
chmod 600 ~/.clave_gemini
source ~/.clave_gemini
cd ~/logistica && bash scripts/probar_gemini.sh
```

> **Resultado esperado:** `Clave encontrada: tipo AQ. (clave nueva de AI Studio)…`, `OK autenticacion con cabecera x-goog-api-key`, `gemini-3.5-flash-lite DISPONIBLE` y `OK generateContent … «OK»`.

Si solo funciona con `?key=` en la URL, el script lo dice: entonces se lanza el transcriptor con `CLAVE_EN_URL=1 bash scripts/voz.sh`. `scripts/voz.sh` carga `~/.clave_gemini` automáticamente.

### 2.2 Micrófono del Jetson

**Probar el micrófono y la transcripción (sin ROS ni brazo)**

```bash
sudo apt install -y alsa-utils          # solo si arecord no existe
arecord -l                              # anotar "tarjeta X ... dispositivo Y" del micrófono USB
arecord -D plughw:X,Y -d 4 -f S16_LE -r 16000 -c 1 ~/prueba.wav    # decir "recoge el cubo rojo"
alsamixer -c X                          # F4 = captura; subir la ganancia si la voz se graba baja
cd ~/logistica && bash scripts/probar_gemini.sh ~/prueba.wav       # OK transcripcion: «recoge el cubo rojo»
```

El dispositivo se pasa luego como `MIC=plughw:X,Y`. Si el micrófono es el predeterminado, se omite. Si el Jetson no tiene micrófono, como respaldo se puede grabar un `.wav` en otra máquina y procesarlo con `bash scripts/voz.sh archivo …`, pero el dictado en vivo es lo que se evalúa.

### 2.3 Dependencias para la figura

```bash
python3 -c "import matplotlib; print('matplotlib OK')" || pip3 install --user matplotlib
```

## 3. Terminales el día del examen

Las terminales A, B y C son **las mismas de la Pregunta 2** (ver su manual). Se agregan D, E y, si se quiere, F.

| Terminal | Qué corre | Comando | Señal de que está bien |
|---|---|---|---|
| A | MoveIt2 (solo planifica) | `bash scripts/moveit.sh` | `You can start planning now!` |
| B | Broker RB-2 | `bash scripts/broker.sh` | `arm_broker listo · política=prioridad · modo=fisico` |
| C | Intérprete (LAYA) | `bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET` | `Servicio /interpretar_orden listo` |
| D | Bag de la Pregunta 3 | `bash scripts/grabar.sh p3` | `Subscribed to topic …` |
| E | Transcriptor de voz | `MIC=plughw:X,Y bash scripts/voz.sh` | `transcriptor_voz listo · … broker=SÍ (/logistica/pick_place …) · inicio de movimiento=MOVER_AGARRE` |
| F (opcional) | Monitor en colores de la transcripción | `source scripts/entorno.sh && python3 herramientas/monitor_voz_api.py` | Verde = Google devolvió texto; amarillo = teclado |

> **Nota:** todas las terminales empiezan con `cd ~/logistica`. Por defecto `voz.sh` envía al broker; `SEGURO=1 bash scripts/voz.sh` transcribe e interpreta sin mover el brazo (útil para ensayar).

## 4. Parte A — usar el transcriptor

```bash
cd ~/logistica
MIC=plughw:X,Y bash scripts/voz.sh
```

Un integrante maneja el teclado: **ENTER** para empezar a grabar cuando el docente va a hablar y **ENTER** apenas termina. El nodo detecta el silencio final del audio y lo descuenta, de modo que "terminó de hablar" es el instante real y no el del ENTER.

**Lo que se ve en la terminal E**

```bash
[ENTER]=grabar · t=escribir orden · q=salir >
  🎙️  GRABANDO… presiona ENTER apenas termine de hablar el docente.
  ☁️  Transcribiendo con Google AI Studio…
  📝 Texto (voz): «recoge el cubo rojo urgente»
  🧠 Decisión: recoger / cubo / rojo · prioridad=68 · permitido=True · LAYA · 142 ms
  📦 Enviada al broker; sigue su avance aquí. Puedes dictar la siguiente.
     ↳ broker [a1b2c3d4] en_cola QUEUED (posición 1)
     ↳ broker [a1b2c3d4] ejecutando DETECTAR_COLOR
     ↳ broker [a1b2c3d4] ejecutando MOVER_AGARRE
  ⏱️  Orden 3: voz → movimiento = 9875.4 ms
```

| Requisito | Dónde se ve la evidencia |
|---|---|
| Clave en variable de entorno | Código (`_clave()` en `transcriptor_voz.py`), `~/.clave_gemini` fuera del repo, salida de `verificar_sin_clave.sh` |
| Tiempo límite propio → modo texto | Log `WARN MODO TEXTO POR TECLADO — …`, tópico `/voz/estado` en el bag, columnas `modo` y `motivo_modo_texto` de `voz_cadena.csv` |
| Transcripción junto al audio | `evidencias/pregunta3/orden_NN_fecha.wav` + `.json` con el mismo nombre |

Variantes útiles:

```bash
bash scripts/voz.sh archivo ~/o1.wav ~/o2.wav      # procesar audios grabados
bash scripts/voz.sh texto                          # fuerza el modo texto (ensayo; NO reemplaza la demo sin internet)
TIMEOUT_VOZ=4.0 bash scripts/voz.sh                # otro tiempo límite de transcripción
MODELO_GEMINI=gemini-3.6-flash bash scripts/voz.sh # otro modelo
```

## 5. Parte B — las cinco órdenes dictadas

1. Terminales A, B, C y D funcionando; cámara/celular grabando el brazo y la pantalla de la terminal E.
2. Apenas el docente dicta cada orden, escribir en la tabla de predicción qué debería pasar (decisión y brazo), **antes de ver el resultado**.
3. En la terminal E: ENTER → el docente dicta → ENTER. Esperar a que la orden termine antes de la siguiente si se quiere medir sin cola.
4. Al final, `q` en la terminal E (espera a que acaben las que siguen en cola) y Ctrl+C en el bag.

| Tipo de orden | Resultado esperado | ¿Cuenta como correcta? |
|---|---|---|
| Válida ("recoge el cubo rojo urgente") | `permitido=True` → entra a la cola con la prioridad del modelo → el brazo deposita ese cubo | Sí, si el cubo correcto llega al depósito |
| Objeto que no está en la mesa ("recoge la botella verde", "el cubo morado") | `permitido=False` · "objeto desconocido…" o "color no configurado" → **rechazo antes de encolar**; el brazo no se mueve | Sí, si se rechaza |
| No permitida ("golpea / lanza / rompe el cubo…", "no recojas…") | `accion=peligrosa` o negación → `permitido=False` → rechazo antes de encolar | Sí, si se rechaza |
| Cubo de un color que se retiró de la mesa | Se encola, el brazo va a escaneo y falla `color no localizado`; no agarra | Explicarlo: el rechazo ocurre en la cámara, no antes de encolar |

Después, abrir `evidencias/pregunta3/voz_cadena.csv` en JupyterLab (clic derecho → Open With → Editor) y completar en cada fila: `lo_que_se_dijo` (literal), `lo_que_hizo_el_brazo` (del video), `resultado_esperado` y `correcta` (sí/no). Luego:

```bash
cd ~/logistica
python3 herramientas/desglose_tiempos.py --csv evidencias/pregunta3/voz_cadena.csv --ordenes N1 N2 N3 N4 N5
# N1..N5 = valores de la columna n de las cinco órdenes del docente -> tabla_cinco_ordenes.md
```

## 6. Modo texto con internet desconectado (entregable obligatorio)

Hay que cortar internet **sin cortar la red del laboratorio**: LAYA está en la red local y debe seguir respondiendo ("la decisión y el movimiento no dependen de internet"). Desconectar el Wi-Fi o el cable del Jetson no sirve: también cortaría LAYA y JupyterLab.

#### Opción recomendada: bloquear Google en el Jetson (reversible, requiere sudo)

```bash
# 1) PREDICCIÓN escrita antes: "el nodo pasará a modo texto en menos de 1 s y el brazo igual se moverá"
echo "0.0.0.0 generativelanguage.googleapis.com" | sudo tee -a /etc/hosts
curl -sS --max-time 5 https://generativelanguage.googleapis.com >/dev/null || echo "Google: SIN ACCESO (bien)"
curl -sS --max-time 5 http://IP_DOCENTE:PUERTO/health && echo "  LAYA: sigue respondiendo (bien)"
# 2) En la terminal E: ENTER, decir una orden, ENTER
#    -> "MODO TEXTO POR TECLADO — ConnectionError: sin internet / Google inaccesible (...)"
#    -> escribir: recoge el cubo azul   -> el brazo debe ejecutarla
# 3) Restaurar internet al terminar:
sudo sed -i "/generativelanguage.googleapis.com/d" /etc/hosts
```

#### Alternativa sin sudo (solo afecta al proceso del transcriptor)

```bash
cd ~/logistica
https_proxy=http://127.0.0.1:9 MIC=plughw:X,Y bash scripts/voz.sh
# toda petición HTTPS del transcriptor falla -> modo texto; LAYA (HTTP, otra terminal) no se ve afectado
```

> **Resultado esperado:** en el video se ven el aviso de modo texto, la orden escrita y el brazo moviéndose. En `voz_cadena.csv` queda una fila con `modo=texto` y `motivo_modo_texto=ConnectionError…`; en el bag, el mensaje `MODO_TEXTO: …` en `/voz/estado`.

## 7. Parte C — ¿dónde se va el tiempo?

### 7.1 Qué mide cada etapa

| Etapa del enunciado | Desde → hasta | Dónde sale |
|---|---|---|
| Captura del audio | Fin real del habla (ENTER − silencio final detectado) → WAV cerrado | `captura_ms` |
| Transcripción en la nube | Envío del audio a Google → texto recibido (red + modelo) | `transcripcion_ms` |
| Decisión del modelo | Llamada a `/interpretar_orden` → respuesta (incluye la red local; `inferencia_ms` es solo el modelo) | `decision_ms`, `inferencia_ms` |
| Envío al broker | Goal enviado → aceptado en la cola | `envio_a_aceptacion_ms` |
| Espera en la cola | Aceptado → primer estado de ejecución (`PLAN_ESCANEO`) | `espera_cola_ms` |
| (Ir a escaneo) | `PLAN_ESCANEO` … `MOVER_ESCANEO` (si el brazo ya está en escaneo es corto) | Figura: movimiento previo / planificación |
| Percepción | `DETECTAR_COLOR` → `LOCALIZADO_…` (proceso de cámara, 6 cuadros, HSV) | Figura: percepción |
| (Pinza) | `ABRIR_PINZA` | Figura: pinza |
| Cinemática inversa | `AGARRE:IK_MOVEIT2_SOLO_PLAN` | Figura: IK |
| Planificación | `PLAN_AGARRE` (FK de la pose enseñada) + `AGARRE:TRAYECTORIA_MOVEIT2_SOLO_PLAN` | Figura: planificación |
| **Inicio del movimiento** | `MOVER_AGARRE`: el brazo va hacia el cubo | `voz_a_movimiento_ms` |

Los tiempos exactos de cada etapa del broker también quedan en `evidencias/pregunta2/<goal_id>/intento.json` (`stages`, `stage_time_s` y, dentro de `planes`, la IK y la trayectoria por separado).

### 7.2 Predicción (escribirla ANTES de medir)

Valores de referencia para razonar la predicción; reemplácenlos por los suyos:

| Etapa | Referencia | Base |
|---|---|---|
| Captura | 0,3 – 1,0 s | Silencio final + reacción del operador + cierre del WAV |
| Transcripción | 1 – 3 s | Viaje a internet + modelo de audio (medir con `probar_gemini.sh prueba.wav`) |
| Decisión (LAYA) | ≈ 0,14 s en calma | P1 en práctica: mediana 137 ms, p95 190 ms; bajo carga sube y puede llegar al límite de 2 s |
| Espera en cola | 0 s con la cola vacía | Con pedidos delante: ≈ un ciclo completo de agarre por cada uno |
| Ir a escaneo | 0,5 – 3 s | Plan MoveIt + movimiento corto si ya estaba en escaneo |
| Percepción | 1,5 – 4 s | Se lanza un proceso Python nuevo que importa OpenCV y abre la cámara en cada pedido |
| Pinza | 0,6 – 2 s | Comando + 0,5 s fijos + espera a que el motor pare |
| IK + planificación | 0,2 – 1,5 s | Servicios de MoveIt (IK con 2 s máximo, plan con 3 s máximo) |

### 7.3 Medir y graficar

```bash
cd ~/logistica
# solo órdenes en modo voz que llegaron a moverse; N = columna n de voz_cadena.csv
python3 herramientas/desglose_tiempos.py --csv evidencias/pregunta3/voz_cadena.csv --ordenes N1 N2 N3
# misma medición hasta el PRIMER movimiento (ir a escaneo):
python3 herramientas/desglose_tiempos.py --csv evidencias/pregunta3/voz_cadena.csv --ordenes N1 N2 N3 \
    --inicio-movimiento MOV --salida-dir evidencias/pregunta3/primer_movimiento
```

Salidas en `evidencias/pregunta3/`: `desglose_tiempos.csv`, `desglose_tiempos.md` (tabla) y `desglose_tiempos.png` (figura). La consola imprime la etapa dominante y, para cada etapa, cuánto quedaría el total si desapareciera (¿alcanza la mitad?). Con pocas órdenes del docente que se movieron, dictar 3–5 órdenes válidas adicionales para tener datos.

### 7.4 Cómo responder (con sus números)

> **Plantilla:** "La etapa dominante fue **[etapa]**, con **[X] ms de [TOTAL] ms ([Y] %)**. Para reducir el tiempo voz → movimiento a la mitad (de [TOTAL] a [TOTAL/2] ms) trabajaríamos sobre **[etapa]**: [acción concreta]. A cambio dejaríamos de obtener **[costo]**."

| Si domina… | Acción | Qué se pierde |
|---|---|---|
| Percepción | Mantener la cámara abierta en un proceso permanente (sin relanzar Python ni OpenCV en cada pedido) | La cámara queda ocupada todo el tiempo; riesgo de usar un cuadro viejo si no se vacía el búfer; más código que validar |
| Transcripción en la nube | Transcripción local en el Jetson (modelo pequeño) o en streaming | Exactitud (más errores de transcripción), carga de GPU/RAM en el Jetson; el streaming depende todavía más de internet |
| Transcripción en la nube | Bajar `timeout_transcripcion_s` | Más caídas a modo texto cuando la red está lenta |
| Captura | Detección automática de fin de habla en lugar de ENTER | Puede cortar al operador si hace pausas |
| Espera en la cola | Más prioridad a la voz o envejecimiento más agresivo | Equidad: los demás clientes esperan más |
| Decisión del modelo | Solo palabras clave, sin LAYA | Robustez ante frases no previstas |
| IK + planificación | Trayectorias precalculadas para las cuatro posiciones | Ya no se comprueban colisiones ni el estado real en cada pedido |

## 8. Checklist de entrega de la Pregunta 3

```bash
cd ~/logistica
ls evidencias/pregunta3/            # orden_*.wav + orden_*.json, voz_cadena.csv, desglose_tiempos.*, tabla_cinco_ordenes.md, bag_p3_*
ros2 bag info evidencias/pregunta3/bag_p3_*     # (con source scripts/entorno.sh) tópicos /voz/* y /logistica/*
bash scripts/verificar_sin_clave.sh  # OK: no hay claves de Google en el proyecto
bash scripts/empaquetar.sh           # ~/logistica_completo.zip para descargar
```

- Código del nodo `transcriptor_voz` (en `src/laya_ordenes/laya_ordenes/`) sin clave.
- Audios `.wav` con su transcripción `.json`.
- Tabla de las cinco órdenes (dicho / transcrito / decisión / brazo / correcta).
- Desglose de tiempos en tabla y figura + respuesta numérica (etapa dominante y qué se sacrificaría).
- Video y fila CSV del modo texto con internet cortado.
- Predicciones escritas antes de medir y su comparación con lo medido.

## 9. Posibles errores y cómo resolverlos

### 9.1 Clave y Google AI Studio

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `FALTA LA CLAVE` / `No hay GEMINI_API_KEY en esta terminal: se usará MODO TEXTO` | No existe `~/.clave_gemini` o no se cargó | Sección 2.1; `voz.sh` la carga sola si el archivo existe |
| `HTTP 400 … API key not valid` | Clave mal copiada, con comillas o espacios | Volver a guardarla con el bloque de la sección 2.1 |
| `HTTP 401 … ACCESS_TOKEN_TYPE_UNSUPPORTED` | Problema conocido de algunas claves nuevas `AQ.` | Probar `CLAVE_EN_URL=1`; si sigue, crear otra clave en aistudio.google.com/apikey (otro proyecto) y repetir `probar_gemini.sh` |
| `HTTP 403 PERMISSION_DENIED` | API no habilitada en el proyecto de la clave o clave restringida | En AI Studio, revisar que la clave no esté bloqueada; crear una nueva |
| `HTTP 404 … model not found` | Nombre de modelo inexistente | `MODELO_GEMINI=gemini-3.6-flash bash scripts/voz.sh`; `probar_gemini.sh` lista los disponibles |
| `HTTP 429 RESOURCE_EXHAUSTED` | Cuota gratuita agotada | Esperar un minuto, usar la clave de otro integrante o `gemini-3.5-flash-lite` (más cuota) |
| `HTTP 500/503` | Google sobrecargado | El nodo pasa a modo texto; reintentar después |
| `MODO TEXTO POR TECLADO — TimeoutError: Google no respondió en 6.0 s` | Red lenta o modelo lento | Es el comportamiento exigido; opcional `TIMEOUT_VOZ=8.0` |
| `MODO TEXTO POR TECLADO — ConnectionError: sin internet / Google inaccesible` | Sin internet (o bloqueo de la sección 6 activo) | Comportamiento exigido; restaurar `/etc/hosts` después de la demo |
| `… devolvió transcripción vacía; probando respaldo` / `RuntimeError: transcripción vacía` | Audio muy bajo, solo ruido o modelo sin salida | Hablar cerca; subir la ganancia con `alsamixer`; el nodo ya prueba el modelo de respaldo |
| `PELIGRO: hay una clave escrita en los archivos de arriba` | Se pegó la clave en un archivo del proyecto | Borrarla de ese archivo; si ya se subió a GitHub, revocarla y crear otra |

### 9.2 Micrófono y audio

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `arecord: command not found` | Falta ALSA | `sudo apt install -y alsa-utils` |
| `arecord no generó audio (revisa: arecord -l y -p dispositivo_alsa)` | Dispositivo equivocado o micrófono desconectado | `arecord -l` y `MIC=plughw:X,Y bash scripts/voz.sh` |
| `arecord: main: audio open error: Device or resource busy` | Otro proceso (notebook, otra grabación) usa el micrófono | Cerrar el otro proceso; un solo transcriptor |
| `audio open error: No such file or directory` | Número de tarjeta/dispositivo incorrecto | Usar los números exactos de `arecord -l` |
| La transcripción sale cortada o rara | Se presionó ENTER antes de que terminara de hablar, o ganancia baja | Esperar un instante después de la última palabra; subir la ganancia |
| `captura_ms` muy grande | El operador tardó en presionar ENTER (no hubo silencio detectable) | Presionar ENTER apenas termine; repetir la medición |

### 9.3 Cadena ROS 2 (intérprete, broker y tiempos)

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `Sin decisión de /interpretar_orden: /interpretar_orden no está disponible en este ROS_DOMAIN_ID` | Terminal C cerrada | `bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET` |
| `sin_broker: La acción del broker no está disponible` | Terminal B cerrada o broker de otra carpeta | `bash scripts/broker.sh` en `~/logistica` (acción `/logistica/pick_place`) |
| `🔒 MODO SEGURO: no se envió al broker` | Se lanzó con `SEGURO=1` | Lanzar `bash scripts/voz.sh` sin `SEGURO=1` |
| `⛔ RECHAZADA antes de encolar: …` | Orden no permitida u objeto ausente | Correcto si la orden debía rechazarse; si era válida, ver la tabla de LAYA del manual P2 (umbral) |
| `voz_a_movimiento_ms` vacío | La orden se rechazó, falló antes de `MOVER_AGARRE` (p. ej. color no localizado) o se usó modo seguro | Normal en rechazos; revisar `estado_broker` y `mensaje_broker` en el CSV |
| `No hay filas con voz_a_movimiento_ms (¿se envió al broker? ¿modo voz?)` | Ninguna orden de voz llegó a moverse, o `--ordenes` con números equivocados | Revisar la columna `n`; usar `--incluir-texto` solo para analizar el modo texto |
| `(matplotlib no está instalado: …)` | Falta matplotlib | `pip3 install --user matplotlib` |
| La orden espera mucho en `QUEUED` | Hay pedidos delante (los integrantes de la P2 siguen enviando) | Para la Parte C, dictar con la cola vacía |
| `Quedaron pedidos sin resultado; revisa el broker antes de reintentar.` | Se salió con `q` antes de que el broker terminara (más de 180 s) | Mirar la terminal B; no reenviar hasta que termine el ciclo |
| Los errores de broker, MoveIt, cámara y LAYA | Mismos de la Pregunta 2 | Ver la sección 9 del manual de la Pregunta 2 |
