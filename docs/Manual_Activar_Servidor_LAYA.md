# Activar el servidor LAYA — guía rápida por computadora

_Windows (laboratorio con o sin GPU), Linux y macOS · verificación desde el Jetson · errores frecuentes_

| Dato | Valor |
|---|---|
| Qué es | Servidor HTTP (no es nodo ROS 2). Responde `POST /v1/systemone` y `GET /health` |
| Dónde corre en el examen | PC Windows del laboratorio; normalmente el docente ya lo dejó corriendo |
| Requisitos | Python 3.10 o más nuevo · internet la PRIMERA vez (descarga el modelo de Hugging Face) · misma red que el Jetson |
| Preset para español | `multilingual` (otros: `english`, `typed-decisions`). En el examen: el que diga el docente |
| Puerto | `8000` (cambiar con `LAYA_PORT` si está ocupado) |
| Quién lo consulta | Solo el nodo `interprete_ordenes` del Jetson (`bash scripts/interprete.sh http://IP:8000 PRESET`) |

> **Cómo usar este manual:** buscar la sección de la computadora que se va a usar, copiar los bloques en orden y terminar siempre con la verificación desde el Jetson (sección 5). La ventana donde corre el servidor queda ocupada: no cerrarla.

## 0. Antes de instalar: ¿ya está corriendo?

Desde una terminal del Jetson (si responde, no hay que activar nada: usar esa IP, ese puerto y el preset de `loaded`):

```bash
curl -sS --max-time 5 http://IP_SERVIDOR:8000/health
```

> **Resultado esperado:** `{"status":"ok","loaded":["multilingual"],"device":"cpu"}` (o `"cuda"`).

| Computadora | Ir a | Notas |
|---|---|---|
| PC Windows del laboratorio (con tarjeta gráfica) | Sección 1 | Primero en CPU; GPU solo si PyTorch ya ve CUDA |
| Laptop Windows del equipo | Sección 1 | CPU; la práctica dio ≈ 121 ms de cálculo por frase |
| Laptop o PC con Linux (Ubuntu) | Sección 2 | CPU, o CUDA si hay NVIDIA con drivers |
| Mac | Sección 3 | Sin `LAYA_DEVICE` (elige solo el dispositivo) |
| El Jetson | No recomendado | Compite en memoria y CPU con ROS 2, MoveIt y la cámara; el examen ubica LAYA en la PC Windows |

## 1. Windows (PowerShell)

Abrir **PowerShell** (no CMD, no la terminal de Jupyter). Todo se copia tal cual.

#### 1.1 Instalar (una sola vez)

```bash
py -0p                                    # lista los Python instalados (se necesita 3.10 o más)
py -3 -m venv "$env:USERPROFILE\laya-servidor-venv"
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -m pip install --upgrade pip
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -m pip install "laya[serve]"
```

Si hay varios Python, elegir uno concreto: `py -3.11 -m venv …` (en el laboratorio funcionó también con 3.14).

#### 1.2 Arrancar en CPU (opción segura)

```bash
$env:LAYA_HOST="0.0.0.0"; $env:LAYA_PORT="8000"; $env:LAYA_DEVICE="cpu"
$env:LAYA_MODELS="multilingual"; $env:LAYA_DEFAULT_MODEL="multilingual"; $env:LAYA_PRELOAD="1"
& "$env:USERPROFILE\laya-servidor-venv\Scripts\laya-serve.exe"
```

> **Nota:** `LAYA_HOST=0.0.0.0` es lo que permite que el Jetson se conecte (con `127.0.0.1` solo responde a la misma PC). La primera vez descarga el modelo: esperar hasta que `/health` muestre `"loaded":["multilingual"]`.

#### 1.3 Arrancar en GPU (solo en la PC con tarjeta NVIDIA)

```bash
& "$env:USERPROFILE\laya-servidor-venv\Scripts\python.exe" -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"
```

Si imprime `True …`: repetir 1.2 cambiando `$env:LAYA_DEVICE="cuda"`. Si imprime `False`: quedarse en CPU (reinstalar PyTorch con CUDA el día del examen puede dejar el servidor inservible).

#### 1.4 Abrir el puerto y anotar la IP

```bash
# PowerShell como ADMINISTRADOR (clic derecho → Ejecutar como administrador):
New-NetFirewallRule -DisplayName "LAYA 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
# PowerShell normal:
ipconfig                                  # "Dirección IPv4" del adaptador de la red del laboratorio (172.51.x.x)
curl.exe http://127.0.0.1:8000/health     # prueba local
Get-NetTCPConnection -LocalPort 8000 -State Listen    # debe aparecer 0.0.0.0:8000
```

#### 1.5 Apagar

`Ctrl+C` en la ventana del servidor. Comprobar con `Get-NetTCPConnection -LocalPort 8000 -State Listen` (no debe devolver nada).

## 2. Linux (Ubuntu)

**Instalar (una sola vez)**

```bash
sudo apt install -y python3-venv python3-pip
python3 -m venv ~/laya-venv
~/laya-venv/bin/python -m pip install --upgrade pip
~/laya-venv/bin/python -m pip install "laya[serve]"
```

**Arrancar (CPU)**

```bash
LAYA_HOST=0.0.0.0 LAYA_PORT=8000 LAYA_DEVICE=cpu LAYA_MODELS=multilingual \
  LAYA_DEFAULT_MODEL=multilingual LAYA_PRELOAD=1 ~/laya-venv/bin/laya-serve
```

**GPU, firewall, IP y prueba local**

```bash
~/laya-venv/bin/python -c "import torch; print(torch.cuda.is_available())"   # True -> usar LAYA_DEVICE=cuda
sudo ufw allow 8000/tcp          # solo si el firewall ufw está activo
hostname -I                      # IP de esta máquina en la red del laboratorio
curl -sS http://127.0.0.1:8000/health
```

## 3. macOS

```bash
python3 -m venv ~/laya-venv
~/laya-venv/bin/python -m pip install --upgrade pip
~/laya-venv/bin/python -m pip install "laya[serve]"
LAYA_HOST=0.0.0.0 LAYA_PORT=8000 LAYA_MODELS=multilingual LAYA_DEFAULT_MODEL=multilingual \
  LAYA_PRELOAD=1 ~/laya-venv/bin/laya-serve
```

Sin `LAYA_DEVICE` el servidor elige el dispositivo disponible; si da error, agregar `LAYA_DEVICE=cpu`. Si macOS pregunta si se aceptan conexiones entrantes: **Permitir**. IP: `ipconfig getifaddr en0` (Wi-Fi). Prueba local: `curl -sS http://127.0.0.1:8000/health`.

## 4. Si el servidor exige clave

Si se arrancó con `LAYA_API_KEY` (Windows: `$env:LAYA_API_KEY="CLAVE"`; Linux/Mac: `LAYA_API_KEY=CLAVE` delante del comando), el Jetson debe enviar la misma clave. En la terminal del intérprete, antes de lanzarlo:

```bash
export LAYA_API_KEY="CLAVE"
```

Sin clave en el servidor no hace falta nada (es lo normal en el laboratorio).

## 5. Verificar desde el Jetson (siempre)

```bash
ping -c 3 IP_SERVIDOR
curl -sS --max-time 5 http://IP_SERVIDOR:8000/health
curl -sS -i --max-time 10 -X POST http://IP_SERVIDOR:8000/v1/systemone -H "Content-Type: application/json" -d '{"state":"recoge el cubo rojo urgente","model":"multilingual","questions":{"accion":{"type":"choice","instructions":"Que accion pide el operador?","criteria":{"recoger":"Agarrar o recoger un objeto","otra":"Otra cosa"}}}}'
```

> **Resultado esperado:** `HTTP/1.1 200 OK` y un JSON con `"answers":{"accion":{"type":"choice","choice":"recoger",…}}`.
> Si entre las cabeceras aparece el tiempo de cálculo del servidor (p. ej. `x-inference-time-ms` o `server-timing`), el nodo lo usa para separar red y cálculo (Pregunta 1, requisito 3).

Luego, en el Jetson, el intérprete:

```bash
cd ~/logistica
bash scripts/interprete.sh http://IP_SERVIDOR:8000 multilingual
```

## 6. Errores frecuentes

| Mensaje o síntoma | Causa | Solución |
|---|---|---|
| `py` / `python` no se reconoce (Windows) | Python no instalado o fuera del PATH | Instalar Python 3.11+ de python.org marcando "Add python.exe to PATH" |
| `laya-serve` no se reconoce | Se llamó sin la ruta del entorno virtual | Usar la ruta completa: `…\laya-servidor-venv\Scripts\laya-serve.exe` o `~/laya-venv/bin/laya-serve` |
| `running scripts is disabled on this system` | Se intentó `Activate.ps1` | No activar el entorno: llamar a los `.exe` con su ruta, como en la sección 1 |
| Error al instalar (`Could not find a version that satisfies…` / falla compilando) | Versión de Python sin paquetes compatibles | Crear el entorno con `py -3.11` (o 3.12) y repetir 1.1 |
| Se queda descargando o `Connection error … huggingface.co` | Primera ejecución sin internet | Conectar a internet una vez; después el modelo queda en caché |
| `[Errno 10048]` / `address already in use` | Otro programa (u otro LAYA) usa el puerto 8000 | Cerrar el otro o usar `LAYA_PORT=8001` (y `http://IP:8001` en el Jetson) |
| `/health` responde en la PC pero no desde el Jetson | Firewall, `LAYA_HOST=127.0.0.1`, otra red o Wi-Fi con aislamiento | Regla de firewall (1.4 / 2), `LAYA_HOST=0.0.0.0`, misma red; probar `ping` |
| `curl: (28) Connection timed out` desde el Jetson | Firewall de Windows bloquea el puerto | Regla de la sección 1.4 (PowerShell como administrador) |
| `curl: (7) Connection refused` | Servidor apagado o escuchando solo en 127.0.0.1 | Arrancarlo con `LAYA_HOST=0.0.0.0` |
| `"loaded":[]` | El modelo aún no se cargó | Esperar; usar `LAYA_PRELOAD=1` y `LAYA_MODELS=multilingual` |
| `Torch not compiled with CUDA enabled` / error de CUDA | PyTorch sin GPU | Volver a `LAYA_DEVICE=cpu` |
| Respuestas lentas o la PC se congela | Poca memoria o CPU saturada | Cerrar programas; un solo preset (`LAYA_MODELS=multilingual`); opcional `LAYA_THREADS=4` |
| `405 Method Not Allowed` en `/v1/systemone` | Se hizo un GET (navegador o curl sin `-X POST`) | Normal: confirma que el servidor está vivo |
| `422 Unprocessable Entity` | JSON mal formado o preset inexistente | Copiar el `curl` de la sección 5 tal cual; preset exacto de `loaded` |
| `401 Unauthorized` | El servidor tiene `LAYA_API_KEY` | Sección 4 |

Referencia: repositorio oficial de LAYA, https://github.com/NandhaKishorM/laya (instalación con `pip install "laya[serve]"`, comando `laya-serve`, variables `LAYA_*`).
