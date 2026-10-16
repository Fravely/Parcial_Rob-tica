# Manual de comandos — Pregunta 1: servicio de interpretación de órdenes

_Resultados esperados, comandos para copiar y pegar, medición de latencia (calma y carga), exactitud LAYA vs palabras clave y errores posibles_

| Dato | Valor |
|---|---|
| JetCobot (Jetson) | `172.51.1.18` · JupyterLab `http://172.51.1.18:8888` · carpeta `~/logistica` |
| ROS_DOMAIN_ID | `72` (lo fija `scripts/entorno.sh`) |
| Nodo y servicio | Nodo `interprete_ordenes` · servicio `/interpretar_orden` · tipo `laya_ordenes_interfaces/srv/InterpretarOrden` |
| Servidor LAYA | IP, puerto y preset que da el docente. Práctica: `http://172.51.1.2:8000`, preset `multilingual` |
| Tiempo límite | Parámetro `timeout_s` = 2,0 s; si LAYA no responde → clasificador por palabras clave, `degradada=True` |
| Evidencias | `evidencias/pregunta1/` (calma.csv, carga.csv, tablas_p1.md, interpretaciones.csv) |

> **Cómo usar este manual:** la sección 1 resume qué se espera obtener, con los números medidos en la práctica. Desde la sección 3, cada bloque gris se copia tal cual en una terminal de JupyterLab (File → New → Terminal). Lo que va en MAYÚSCULAS (IP_DOCENTE, PUERTO, PRESET) se reemplaza por el dato del docente.

## 1. Resultados esperados

### 1.1 Por requisito

| Requisito | Cómo lo cumple el nodo | Resultado esperado (lo que se debe ver) |
|---|---|---|
| Nodo `interprete_ordenes` con el servicio `/interpretar_orden` | `scripts/interprete.sh` lanza `laya_ordenes/node.py` con `-r __node:=interprete_ordenes` | `ros2 node list` muestra `/interprete_ordenes`; `ros2 service type /interpretar_orden` devuelve `laya_ordenes_interfaces/srv/InterpretarOrden` |
| Decisión tipada: acción, objeto, color, prioridad (entero), permitido (booleano) | La respuesta trae esos campos más `degradada`, `fuente`, `motivo` y tres latencias | `accion='recoger', objeto='cubo', color='rojo', prioridad=68, permitido=True, degradada=False, fuente='LAYA'` |
| R1. LAYA no genera texto | Solo hace preguntas cerradas: `choice` (acción, objeto, color), `score` (prioridad) y `noul` (sí/no de autorización). Nunca pide redactar | Ninguna respuesta de LAYA trae texto libre; toda salida está dentro de una lista de opciones |
| R2. Tiempo límite declarado como parámetro; respaldo por palabras clave; nunca se queda esperando | Parámetro `timeout_s` (2,0 s), configurable en caliente con `ros2 param set` | Con LAYA caído o lento: `degradada=True`, `fuente='respaldo'`, motivo `modo degradado (TimeoutError…)` y respuesta en ≈ 2 000 ms como máximo (en la práctica: 2 002–2 007 ms) |
| R3. Latencia sobre 50 frases: mediana y p95; separar red y cálculo del servidor | `latencia_http_ms` (ida y vuelta HTTP medida por el nodo), `inferencia_ms` (cálculo que informa el servidor), `resto_http_ms` = diferencia | Tabla con mediana y p95 de las cuatro medidas (ver 1.2) |
| R4. Calma vs. todos los equipos a la vez | Mismo script en modo `calma` y en modo `carga` | Bajo carga sube sobre todo el p95 y el "resto" (cola en el servidor); aparecen respuestas degradadas por timeout |
| R5. Exactitud LAYA vs. palabras clave | `evaluar_pregunta1.py` corre ambos métodos sobre las mismas 50 frases; `tablas_pregunta1.py` arma la tabla | Tabla comparativa con aciertos por campo, falsos permitidos y falsos rechazos |

### 1.2 Números de referencia (práctica, laboratorio en calma, 50 frases)

Medidos con este mismo nodo contra el LAYA de práctica (`172.51.1.2:8000`, preset `multilingual`, CPU). El día del examen cambian, pero el orden de magnitud y el patrón deberían repetirse:

| Medida | Mediana | p95 | Qué significa |
|---|---|---|---|
| Servicio `/interpretar_orden` (cliente ROS 2) | 137 ms | 190 ms | Lo que espera quien llama al servicio |
| Ida y vuelta HTTP a LAYA | 133 ms | 186 ms | Red + cola del servidor + cálculo |
| Cálculo informado por el servidor | 121 ms | 153 ms | Solo el modelo (cabecera de tiempo de LAYA) |
| Resto = HTTP − cálculo | 11 ms | 21 ms | Red local + espera en el servidor + serialización (no es solo red) |

La primera petición del día tardó 661 ms (conexión y modelo "en frío"); por eso el script hace una petición de calentamiento que no se cuenta.

#### Bajo carga (predicción razonada, aún no medida)

- El **cálculo** del servidor cambia poco por petición (el modelo es el mismo), aunque puede subir si la CPU/GPU se reparte entre equipos.
- El **resto** (cola en el servidor) es lo que más crece: el servidor atiende a todos los equipos y las peticiones esperan su turno.
- El **p95 sube mucho más que la mediana**. Toda petición que supere 2 s se corta y sale del respaldo: su latencia queda en ≈ 2 000 ms, de modo que el p95 bajo carga puede quedar "pegado" al tiempo límite.
- La exactitud de LAYA no cambia por la carga; lo que cambia es **cuántas** respuestas son de LAYA y cuántas degradadas.

#### Exactitud en la práctica (acierto = acción, objeto, color y permitido correctos)

| Método | n | Aciertos | Exactitud | Observación |
|---|---|---|---|---|
| LAYA (respuestas reales, no degradadas) | 29 | 11 | 37,9 % | 21 de 50 frases se degradaron por baja confianza (< 0,5) |
| Palabras clave, versión de la práctica | 50 | 30 | 60,0 % | Antes del parche (femenino, "fuerza", "para", "mueve") |
| Palabras clave, versión actual | 50 | 50 | 100 % | Medido sobre el mismo conjunto con el que se ajustó: esperar menos con las frases del docente |
| Servicio completo (LAYA + respaldo) con la versión actual | 50 | 32 | 64 % | Estimado a partir de la corrida de práctica |

Por campo, LAYA acertó **acción 23/29, objeto 27/29, color 27/29 y permitido 17/29**: casi todos sus errores están en la autorización sí/no (11 falsos rechazos y 1 falso permitido).

#### Qué tipo de frases falla cada método (base para la media página de comentario)

| Método | Falla en… | Ejemplos de la práctica |
|---|---|---|
| LAYA | La pregunta sí/no de autorización: no separa órdenes válidas de peligrosas (válidas recibieron 0,08–0,57; peligrosas 0,40–0,52) | "deja la caja azul en la mesa" (sí = 0,08), "toma la botella azul" (0,17) rechazadas |
| LAYA | Acciones con modificadores o verbos menos frecuentes | "levanta el cubo verde con cuidado" → detener; "arroja el cubo" → recoger; "traslada … urgentemente" → recoger |
| LAYA | Baja confianza en verbos de colocar (deja, deposita, traslada, pon, mueve) → la frase se degrada al respaldo | 17 de las 21 degradaciones fueron por la acción |
| Palabras clave | Sinónimos o verbos que no están en la lista, frases sin palabra clave explícita, errores de escritura o de transcripción | "coge", "sujeta", "alcánzame" no están en la lista |
| Palabras clave | Negaciones o peligros expresados de otra forma | "evita tomar…", "con mucha fuerza" |
| Ambos | Distinguir "objeto fuera del inventario" (`otro`) de "no se nombró objeto" (`ninguno`) | "recoge el avión morado", "coloca la botella" (sin color) |

> **Nota:** el parche y la regla `otro`/`ninguno` del respaldo se ajustaron con estas 50 frases de práctica. Con las 50 del docente la exactitud de las palabras clave será menor; eso es justamente lo que hay que comentar.

## 2. Antes del examen: preparación

### 2.1 Proyecto compilado en el Jetson

Si ya se siguió el manual de la Pregunta 2 (sección 2), este paso está hecho. Si no:

```bash
cd ~
[ -d ~/logistica ] && mv ~/logistica ~/logistica_old_$(date +%m%d_%H%M)
unzip -q logistica.zip
cd ~/logistica
sed -i "s/\r$//" scripts/*.sh
bash scripts/compilar.sh --limpio
python3 -m unittest discover -s tests -v          # 20 pruebas OK (lógica del intérprete, sin ROS)
```

### 2.2 El archivo con las 50 frases del docente

El evaluador necesita un CSV con estas columnas exactas (la primera fila es el encabezado):

**Formato (ejemplo de 4 filas)**

```bash
frase,accion_esperada,objeto_esperado,color_esperado,prioridad_esperada,permitido_esperado
recoge el cubo rojo urgente,recoger,cubo,rojo,,True
golpea la botella azul,peligrosa,botella,azul,,False
recoge el avion morado,recoger,otro,otro,,False
detén el brazo,detener,ninguno,ninguno,,False
```

| Columna | Valores válidos |
|---|---|
| `accion_esperada` | `recoger`, `colocar`, `detener`, `peligrosa`, `otra` |
| `objeto_esperado` | un objeto del inventario (p. ej. `cubo`), `otro` (se nombra algo que no está en la mesa) o `ninguno` (no se nombra objeto) |
| `color_esperado` | `rojo`, `azul`, `verde`, `amarillo`, `otro` (otro color) o `ninguno` (no se dice color) |
| `prioridad_esperada` | opcional (puede quedar vacía): no entra en la exactitud porque LAYA y las palabras clave usan escalas distintas |
| `permitido_esperado` | `True` o `False` |

**Crear el archivo**

```bash
cd ~/logistica
cp evidencias/pregunta1/plantilla_50_frases_docente.csv evidencias/pregunta1/50_frases_docente.csv
# abrirlo en JupyterLab: clic derecho → Open With → Editor, llenar las 50 filas y guardar (Ctrl+S)
```

Si se llena en Excel: *Guardar como → CSV UTF-8 (delimitado por comas)* y subirlo a `~/logistica/evidencias/pregunta1/`. Para ensayar antes del examen ya existe un conjunto de práctica: `evidencias/pregunta1/50_peticiones_practica_LAYA.csv`.

### 2.3 El inventario debe ser el mismo en el nodo y en el evaluador

`permitido` depende de qué objetos se consideran "sobre la mesa". Se fija con la variable `OBJETOS` y se usa **la misma** al lanzar el intérprete y al evaluar:

| Caso | Valor de OBJETOS |
|---|---|
| Mesa del examen (cuatro cubos de colores) | `OBJETOS="cubo"` (es el valor por defecto) |
| Las 50 frases de práctica (cubo, botella, pelota, caja) | `OBJETOS="cubo botella pelota caja"` |
| Frases del docente | Los objetos que el docente considere disponibles en sus etiquetas |

## 3. Terminal A — arrancar el intérprete

**Día del examen**

```bash
cd ~/logistica
OBJETOS="cubo" bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET
```

**Ensayo con los datos de práctica**

```bash
cd ~/logistica
OBJETOS="cubo botella pelota caja" bash scripts/interprete.sh http://172.51.1.2:8000 multilingual
```

> **Resultado esperado:** primero muestra `Inventario del interprete: ['cubo']` y la respuesta de `/health` (algo como `{"status":"ok","loaded":["multilingual"],…}`); luego:
> `Servicio /interpretar_orden listo. URL=http://IP:PUERTO, timeout=2.00s, umbral_si=0.60, inventario=['cubo']. No mueve el brazo.`
> Dejar esta terminal abierta todo el examen.

Opciones (se escriben delante del comando, siempre con decimales): `TIMEOUT_LAYA=2.0` (tiempo límite), `UMBRAL_LAYA=0.60` (sí mínimo de LAYA para permitir), `CONFIANZA_LAYA=0.50` (confianza mínima de cada elección). Si el servidor exige clave: `export LAYA_API_KEY="CLAVE_DEL_SERVIDOR"` antes del comando.

## 4. Terminal B — comprobar el nodo y el servicio

```bash
cd ~/logistica && source scripts/entorno.sh
ros2 node list | grep interprete                # /interprete_ordenes
ros2 service type /interpretar_orden            # laya_ordenes_interfaces/srv/InterpretarOrden
ros2 interface show laya_ordenes_interfaces/srv/InterpretarOrden
ros2 param get /interprete_ordenes timeout_s    # Double value is: 2.0
ros2 param get /interprete_ordenes url_laya     # String value is: http://IP:PUERTO
```

**Una frase**

```bash
ros2 service call /interpretar_orden laya_ordenes_interfaces/srv/InterpretarOrden "{frase: 'recoge el cubo rojo urgente'}"
```

> **Resultado esperado:** `response: laya_ordenes_interfaces.srv.InterpretarOrden_Response(accion='recoger', objeto='cubo', color='rojo', prioridad=68, permitido=True, degradada=False, fuente='LAYA', motivo='orden autorizable; …', latencia_http_ms=150.4, inferencia_ms=125.7, resto_http_ms=24.7)`

**Seis frases seguidas**

```bash
bash scripts/probar_interprete.sh
```

| Frase (la manda el script) | Resultado esperado con OBJETOS="cubo" |
|---|---|
| recoge el cubo rojo urgente | `permitido=True`, `fuente='LAYA'`; prioridad mayor que una normal |
| recoge el cubo azul · toma el cubo verde sin prisa · agarra el cubo amarillo | `permitido=True`, `fuente='LAYA'` (si sale "LAYA no autoriza", ver 10.2) |
| recoge la botella verde | `permitido=False`: objeto fuera del inventario (`otro`/`ninguno`) |
| golpea el cubo rojo | `accion='peligrosa'`, `permitido=False` |

Otras frases útiles para probar a mano: "no recojas el cubo azul" (`permitido=False` por negación o porque LAYA no autoriza), "qué hora es" (`accion='otra'`, `permitido=False`), "recoge el cubo morado" (`color='otro'`, `permitido=False`).

## 5. Requisito 2 — demostrar el tiempo límite y el respaldo

El nodo lee `timeout_s` en cada petición, así que se puede bajar en caliente para forzar el corte (LAYA tarda ≈ 130 ms; con 0,1 s siempre se pasa):

```bash
cd ~/logistica && source scripts/entorno.sh
ros2 param set /interprete_ordenes timeout_s 0.1
ros2 service call /interpretar_orden laya_ordenes_interfaces/srv/InterpretarOrden "{frase: 'recoge el cubo azul'}"
# -> degradada=True, fuente='respaldo', motivo='modo degradado (TimeoutError: LAYA superó timeout_s=0.10); …'
ros2 param set /interprete_ordenes timeout_s 2.0
ros2 service call /interpretar_orden laya_ordenes_interfaces/srv/InterpretarOrden "{frase: 'recoge el cubo azul'}"
# -> otra vez degradada=False, fuente='LAYA'
```

Segunda forma (servidor apagado o inalcanzable): con LAYA detenido, la respuesta sale del respaldo en pocos milisegundos con motivo `URLError … Connection refused`. Ambas quedan registradas en `evidencias/pregunta1/interpretaciones.csv` (columnas `degradada`, `fuente`, `motivo`, `latencia_servicio_ms`).

## 6. Predicciones (escribirlas ANTES de medir)

El examen califica la diferencia entre lo predicho y lo medido. Copiar esta tabla en el informe, llenarla con hora y recién después ejecutar la sección 7:

| Medida | Predicción en calma | Predicción bajo carga | Base |
|---|---|---|---|
| Servicio: mediana / p95 | ___ / ___ ms | ___ / ___ ms | Práctica: 137 / 190 ms |
| HTTP: mediana / p95 | ___ / ___ ms | ___ / ___ ms | Práctica: 133 / 186 ms |
| Cálculo del servidor: mediana / p95 | ___ / ___ ms | ___ / ___ ms | Práctica: 121 / 153 ms |
| Resto (red + cola): mediana / p95 | ___ / ___ ms | ___ / ___ ms | Práctica: 11 / 21 ms |
| Respuestas degradadas | ___ / 50 | ___ / 50 | Práctica: 21/50 por baja confianza, 0 por timeout |
| Exactitud LAYA / palabras clave | ___ % / ___ % | (igual) | Práctica: 38 % / 60–100 % |

## 7. Medir las 50 frases

### 7.1 En calma

```bash
cd ~/logistica
OBJETOS="cubo" bash scripts/evaluar_p1.sh calma evidencias/pregunta1/50_frases_docente.csv
```

> **Resultado esperado:** una línea por frase y un resumen final:
> `[01/50] calma: LAYA, 141.2 ms` … `[50/50] calma: respaldo, 138.9 ms`
> `LAYA real: NN/50; respaldo: MM/50; sin respuesta: 0/50` y la ruta de `calma.csv` y `calma_tabla_resumen.csv`.

### 7.2 Bajo carga (cuando el docente indique que todos los equipos consultan a la vez)

```bash
cd ~/logistica
OBJETOS="cubo" bash scripts/evaluar_p1.sh carga evidencias/pregunta1/50_frases_docente.csv
```

Una sola persona del equipo ejecuta la medición; la carga la ponen los demás equipos consultando el mismo servidor. Anotar la hora de inicio y cuántos equipos estaban consultando. Si una corrida se repite, el script guarda la anterior con otro nombre (no se pierde).

### 7.3 Tablas para el informe

```bash
cd ~/logistica
python3 herramientas/tablas_pregunta1.py
cat evidencias/pregunta1/tablas_p1.md
```

Genera `tablas_p1.md` (latencia calma vs. carga, exactitud LAYA vs. palabras clave y la lista de frases que falla cada método), `tablas_p1_latencia.csv` y `tablas_p1_exactitud.csv`. El CSV de las 50 frases con la decisión de cada método es `evidencias/pregunta1/calma.csv` (columnas `*_laya` y `*_respaldo`).

> **Nota:** si LAYA degrada muchas frases por "confianza insuficiente", se puede repetir la corrida en calma con `CONFIANZA_LAYA=0.35` (reiniciando la terminal A) y reportar ambas. Igual con `UMBRAL_LAYA=0.30` si rechaza órdenes válidas.
> Cualquier ajuste se declara en el informe con su motivo.

## 8. Textos de apoyo para el informe

#### Requisito 1: por qué la salida debe ser una decisión tipada

Un robot solo puede ejecutar decisiones que el programa entiende sin ambigüedad. Si LAYA redactara texto libre, habría que volver a interpretarlo (otra fuente de error), podría inventar objetos o acciones que no existen en la mesa, su tiempo de respuesta crecería con la longitud del texto y su salida no se podría validar contra el inventario ni contra las reglas de seguridad. Con preguntas cerradas (elección, puntaje, sí/no) el espacio de respuestas es finito y conocido, se valida campo por campo, se mide la confianza de cada elección y el costo de cálculo es una sola pasada, acotado y predecible. Además, una instrucción maliciosa escrita en la frase no puede convertirse en un comando nuevo: como mucho cambia la elección entre opciones permitidas, y las reglas locales siguen vetando lo peligroso.

#### Requisito 4: cómo explicar la diferencia calma / carga

Plantilla: "En calma la mediana del servicio fue [X] ms y el p95 [Y] ms; bajo carga, [X'] y [Y']. El cálculo del servidor pasó de [a] a [a'] ms, mientras que el resto (red + cola) pasó de [r] a [r'] ms: el aumento se debe principalmente a la espera en el servidor compartido, no a la red local ni al modelo. [N] frases superaron el tiempo límite de 2 s y se resolvieron con el respaldo; por eso el p95 bajo carga queda en ≈ 2 000 ms."

#### Requisito 5: comentario de media página

Usar la sección 3 de `tablas_p1.md` (frases que falla cada método) y la tabla 1.2 de este manual: LAYA entiende paráfrasis y sinónimos, pero su sí/no de autorización no discrimina bien y se degrada en verbos de colocar; las palabras clave son exactas con el vocabulario previsto y fallan con sinónimos, negaciones indirectas o errores de transcripción.

## 9. Checklist de entrega de la Pregunta 1

- Código del nodo: `src/laya_ordenes/laya_ordenes/node.py` y `logic.py` (+ `config/interprete_ordenes_logistica.yaml`).
- `evidencias/pregunta1/calma.csv` y `carga.csv`: las 50 frases con la decisión de LAYA y la del clasificador por palabras clave.
- `evidencias/pregunta1/tablas_p1.md`: latencia en calma y bajo carga (mediana y p95) y exactitud comparada.
- Predicciones escritas antes de medir y su comparación con lo medido.
- Demostración del tiempo límite (sección 5) con su fila en `interpretaciones.csv`.
- Media página de comentario sobre qué frases falla cada método.

## 10. Posibles errores y cómo resolverlos

### 10.1 Arranque del intérprete

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `AVISO: http://…/health no respondio` | IP/puerto equivocados, servidor apagado o firewall de Windows | `ping -c 3 IP_DOCENTE`; `curl -v --connect-timeout 5 http://IP:PUERTO/health`; ver el manual de activación de LAYA |
| `AVISO: sin URL de LAYA. Todas las decisiones saldran degradadas` | Se lanzó sin URL | `bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET` |
| `InvalidParameterTypeException` o `Wrong parameter type` al arrancar | Se pasó un entero donde va decimal (p. ej. `UMBRAL_LAYA=1`) | Escribir siempre con decimales: `1.0`, `0.30`, `2.0` |
| Dos líneas en `ros2 node list` con `interprete_ordenes` | Quedó otro intérprete abierto (otra terminal o proyecto viejo) | Ctrl+C en el sobrante; un solo intérprete por dominio |
| `Package 'laya_ordenes' not found` | No se compiló o no se cargó el proyecto | `bash scripts/compilar.sh --limpio` |
| `Inventario vacío: no se autorizarán movimientos.` | `OBJETOS` vacío | `OBJETOS="cubo" bash scripts/interprete.sh …` |

### 10.2 Respuestas del servicio

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `modo degradado (TimeoutError: LAYA superó timeout_s=2.00)` | LAYA tardó más de 2 s (saturado o lejos) | Es el respaldo exigido. Si pasa en calma: revisar la red; opcional `TIMEOUT_LAYA=3.0` |
| `modo degradado (URLError: … Connection refused)` | El servidor no corre o escucha solo en 127.0.0.1 | En el servidor: `LAYA_HOST=0.0.0.0` (manual de activación) |
| `modo degradado (URLError: … No route to host / timed out)` | El Jetson y el servidor no están en la misma red, o firewall | `ping`; regla de firewall para el puerto; misma red Wi-Fi/cable |
| `modo degradado (HTTPError: HTTP Error 401)` | El servidor se arrancó con `LAYA_API_KEY` | `export LAYA_API_KEY="…"` en la terminal A y relanzar |
| `modo degradado (HTTPError: HTTP Error 422)` | Petición rechazada (preset inexistente o formato) | Usar el preset exacto que muestra `loaded` en `/health` |
| `modo degradado (ValueError: accion: confianza insuficiente)` | LAYA eligió con confianza < 0,5 | Es un resultado válido (se reporta). Opcional: `CONFIANZA_LAYA=0.35` |
| `LAYA no autoriza (probabilidad sí=0.27 < umbral 0.60)` en una orden válida | El sí/no de LAYA no discrimina bien | Reportarlo; opcional `UMBRAL_LAYA=0.30` (las reglas locales siguen vetando lo peligroso) |
| `modo degradado (TimeoutError: sin cupos HTTP; servidor saturado)` | Más de 4 consultas simultáneas desde este nodo (P2/P3 con varios clientes) | Normal bajo uso intenso; el respaldo responde |
| `modo degradado (ValueError: timeout_s debe estar entre 0.1 y 120.0 segundos)` | Se puso `timeout_s` fuera de rango con `ros2 param set` | `ros2 param set /interprete_ordenes timeout_s 2.0` |
| `inferencia_ms=-1.0` y `resto_http_ms=-1.0` con `fuente='LAYA'` | El servidor no envió la cabecera con su tiempo de cálculo | No se puede separar red y cálculo: decirlo en el informe y consultar al docente la versión del servidor |
| `Setting parameter failed: Wrong parameter type` | `ros2 param set … timeout_s 2` (entero) | Usar `2.0` |

### 10.3 Evaluación de las 50 frases

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `ERROR: no existe …/50_frases_docente.csv` | Falta crear el archivo | Sección 2.2 |
| `CSV incorrecto; columnas requeridas: frase,accion_esperada,…` | Encabezado distinto, otro separador o archivo de Excel (.xlsx) | Copiar el encabezado de la sección 2.2; guardar como "CSV UTF-8"; el script acepta `,` o `;` |
| `Deben ser 50 frases REALES del docente; el CSV contiene N.` | Filas vacías al final o frases faltantes | Borrar las filas vacías; deben quedar 50 + encabezado |
| `Hay frases vacías en el CSV.` | Una fila sin frase | Completarla o borrarla |
| `No está disponible /interpretar_orden en el ROS_DOMAIN_ID actual.` | Terminal A cerrada | Sección 3 |
| `[NN/50] calma: sin respuesta` / `Sin respuesta ROS en 10.0s` | El nodo no respondió a tiempo | Revisar la terminal A; opcional `TIMEOUT_CLIENTE=15` |
| `LAYA real: 0/50; respaldo: 50/50` | Todas degradadas: LAYA inalcanzable o URL equivocada | Revisar `/health` y la URL antes de repetir |
| `ModuleNotFoundError: No module named 'laya_ordenes'` o `rclpy` | Se ejecutó `python3 herramientas/…` sin cargar el proyecto | Usar `bash scripts/evaluar_p1.sh …` (carga todo) |
| Exactitud de palabras clave muy baja con frases buenas | El inventario (`OBJETOS`) no coincide con el de las etiquetas | Usar el mismo `OBJETOS` en el intérprete y en la evaluación |
| `No hay corridas: ejecuta primero …` (tablas) | Falta `calma.csv` | Ejecutar 7.1 antes de 7.3 |
