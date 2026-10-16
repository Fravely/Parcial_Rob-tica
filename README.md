# logistica — JetCobot · ROS 2 Humble · Broker RB-2 + LAYA + voz

Proyecto del examen parcial (Gran Reto JetCobot). Es la **fusión** de dos carpetas:

- `logistica_sinLaya1`: el broker del RB-2 que **ya movió el brazo** (cola con prioridad,
  un solo worker, cámara, IK/MoveIt2 solo para planificar y ejecución por pymycobot).
- `logistica`: el intérprete LAYA (Pregunta 1), los clientes y el transcriptor de voz
  (Pregunta 3).

**JetCobot:** `172.51.1.18` · **JupyterLab:** `http://172.51.1.18:8888` ·
**ROS_DOMAIN_ID:** `72` · **acción del broker:** `/logistica/pick_place`.

Manuales completos (comandos por terminal y cuadro de errores):

- `docs/Manual_Pregunta1_Interprete.docx` (y `.md`): resultados esperados, 50 frases, calma/carga, exactitud.
- `docs/Manual_Activar_Servidor_LAYA.docx` (y `.md`): guía rápida para Windows, Linux y macOS.
- `docs/Manual_Pregunta2_con_LAYA.docx` (y `.md`)
- `docs/Manual_Pregunta3_Voz.docx` (y `.md`), incluye el análisis de lo que falta.

## Cadena completa

```
voz ─► transcriptor_voz ──HTTPS──► Google AI Studio (texto)
          │
texto ─► /interpretar_orden (interprete_ordenes) ──HTTP──► LAYA (PC Windows)
          │      └─ si LAYA no responde a tiempo: respaldo por palabras clave (degradada)
          ▼
   permitido=False ─► RECHAZADA ANTES DE ENCOLAR (con su causa)
   permitido=True  ─► /logistica/pick_place (broker RB-2, prioridad = la del modelo)
                         └─ UN worker: escaneo → cámara → IK/plan MoveIt2 → pinza → depósito
```

Solo el worker del broker abre `/dev/ttyUSB0`. Clientes, intérprete y MoveIt nunca
mandan comandos al brazo.

## Uso rápido (todas las terminales: `cd ~/logistica`)

| Terminal | Comando |
|---|---|
| (una vez) | `bash scripts/compilar.sh --limpio` |
| A · MoveIt2 | `bash scripts/moveit.sh` |
| B · Broker | `bash scripts/broker.sh` |
| C · Intérprete LAYA | `bash scripts/interprete.sh http://IP_DOCENTE:PUERTO PRESET` |
| D · Bag | `bash scripts/grabar.sh p2` (o `p3`) |
| E–H · Integrantes (P2) | `bash scripts/cliente.sh integrante1` … `integrante4` |
| Voz (P3) | `MIC=plughw:X,Y bash scripts/voz.sh` |
| Ver la cola | `bash scripts/ver_cola.sh` |

Pregunta 1: `OBJETOS="cubo" bash scripts/evaluar_p1.sh calma|carga` y `python3 herramientas/tablas_pregunta1.py`.
Otros scripts: `probar_interprete.sh` (6 frases de prueba), `probar_gemini.sh`
(clave e internet, sin ROS), `cliente_sin_laya.sh` (respaldo sin LAYA),
`verificar_sin_clave.sh` (antes de entregar), `empaquetar.sh` (ZIP sin build).

## Clave de Google AI Studio

Nunca en el repositorio. Se guarda en el Jetson, en `~/.clave_gemini`
(`export GEMINI_API_KEY="..."`, permisos 600). `scripts/voz.sh` la carga.
Antes de cada entrega: `bash scripts/verificar_sin_clave.sh` (detecta claves `AQ.` y `AIza`).

## Archivos principales

| Archivo | Para qué |
|---|---|
| `src/arm_broker/arm_broker/broker.py` | Broker RB-2 (igual al de `logistica_sinLaya1`) |
| `src/arm_broker/arm_broker/orden_local.py`, `cliente_sin_laya.py` | Modo sin LAYA (respaldo) |
| `src/laya_ordenes/laya_ordenes/node.py`, `logic.py` | Intérprete `/interpretar_orden` (LAYA + respaldo) |
| `src/laya_ordenes/laya_ordenes/cliente_laya.py` | Cliente de cada integrante (P2) |
| `src/laya_ordenes/laya_ordenes/transcriptor_voz.py`, `cadena.py` | Nodo de voz (P3) |
| `config/broker.yaml`, `config/poses.json` | Política, inventario, MoveIt; poses enseñadas y regiones de cámara |
| `config/interprete_ordenes_logistica.yaml` | Inventario de la mesa (`cubo`) y umbrales del intérprete |
| `herramientas/resumen_item2.py` | Tabla de los diez intentos (P2) |
| `herramientas/desglose_tiempos.py` | Tabla y figura de tiempos (P3, Parte C) |
| `reparar_moveit.py`, `recuperar_cubo.py` | Límites de MoveIt; recuperar un cubo sujeto |

## Pruebas sin robot

```bash
python3 -m unittest discover -s tests -v
python3 herramientas/probar_broker_sin_ros.py
python3 herramientas/pruebas_sin_ros/prueba_cliente_laya.py
python3 herramientas/pruebas_sin_ros/prueba_p3_sin_ros.py
```

Detalle de los cambios de la fusión: `CAMBIOS_FUSION.md`. Documentos anteriores:
`docs/historico/`. La versión anterior del broker de esta carpeta (regiones, 13-oct)
quedó en `ref/broker_logistica_regiones_13oct.py`.
