# Fusión logistica + logistica_sinLaya1 (15-oct-2026)

## Qué se tomó de cada carpeta

| De `logistica_sinLaya1` (funciona en el brazo) | De `logistica` (LAYA y voz) |
|---|---|
| `broker.py` completo (sin cambios de código), `orden_local.py`, `cliente_sin_laya.py` | Paquetes `laya_ordenes` y `laya_ordenes_interfaces` (reactivados) |
| Poses (`config/poses.json` = `poses_sin_laya.json`) y parámetros (`config/broker.yaml`) | Evidencias de la Pregunta 1, herramientas de medición |
| Scripts de terminal, `reparar_moveit.py`, `recuperar_cubo.py` | `transcriptor_voz`, `cadena`, `interfaz_ordenes`, `desglose_tiempos` |

`fk.py`, `politicas.py`, `cliente.py` e interfaces (`MoveArm`, `PickPlace`, `QueueState`)
eran idénticos en ambas carpetas.

## Cambios hechos al fusionar

1. **Espacio de nombres `/logistica`** para la acción, la cola y las lecturas del brazo
   (antes `/sin_laya`). MoveIt lee el estado desde `/logistica/arm/measured_joint_states`.
2. **Cliente LAYA por integrante** (`laya_ordenes/cliente_laya.py`, `scripts/cliente.sh`):
   texto → `/interpretar_orden` → si está permitido, goal al broker con la prioridad del modelo;
   si no, rechazo antes de encolar con su causa. CSV por integrante en `evidencias/pregunta2/clientes/`.
3. **Prioridad unificada**: LAYA (score × 50), respaldo y modo local usan la misma escala
   (20 / 80 / 180 en reglas). `tau_envejecimiento_s: 0.2` → 50 puntos ≈ 10 s de espera.
4. **Acciones admitidas**: `recoger` y `colocar` (misma tarea física: llevar al depósito).
5. **Intérprete**: inventario real (`cubo`), parámetro `umbral_autorizacion` (LAYA negó órdenes
   válidas en la práctica), parche del respaldo aplicado (prohibidas, femenino, "para", "mueve",
   "lleva") y rechazo de órdenes con dos colores.
6. **Transcriptor**: acción `/logistica/pick_place`, cola derivada de la acción, inicio de
   movimiento = `MOVER_AGARRE` (configurable), opción `clave_en_url`.
7. **`desglose_tiempos.py`**: por defecto mide hasta `MOVER_AGARRE`.
8. **`reparar_moveit.py`**: corregido (leía `recogida_grados`, que ya no existe); escribe
   `config/moveit_local.yaml`. `scripts/moveit.sh` reutiliza `~/logistica_sinLaya1/config/moveit_sin_laya.yaml` si existe.
9. **Seguridad de clave**: `.gitignore`, `scripts/verificar_sin_clave.sh` (claves `AQ.` y `AIza`),
   `scripts/probar_gemini.sh` (prueba sin ROS, nunca imprime la clave).
10. **Dominio 72** en todas las herramientas (había `52` fijo).
11. `broker.sh` se niega a arrancar si sigue abierto el broker de `logistica_sinLaya1`.
12. Evidencias por pregunta: `evidencias/pregunta1`, `pregunta2`, `pregunta3`.

No se modificó la lógica del broker (`broker.py` es byte a byte el de `logistica_sinLaya1`,
solo con fines de línea Unix).

## Agregado para la Pregunta 1 (15-oct, segunda parte)

13. `scripts/evaluar_p1.sh calma|carga` (calienta la conexión, guarda la corrida anterior) y
    `herramientas/tablas_pregunta1.py` (latencia calma/carga, exactitud LAYA vs palabras clave,
    frases que falla cada método).
14. `scripts/interprete.sh` acepta `OBJETOS` (inventario) y `CONFIANZA_LAYA`; solo pasa URL y
    preset si tienen valor.
15. Respaldo: distingue `otro` (se nombra algo fuera del inventario o un color no configurado) de
    `ninguno` (no se nombra), igual que las opciones que se le dan a LAYA.
16. `evaluar_pregunta1.py` acepta CSV separados por `;` (Excel en español).
