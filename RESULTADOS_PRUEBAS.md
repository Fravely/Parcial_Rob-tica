# Pruebas de software de la fusión — 15/10/2026

Sin ROS ni hardware (dobles de prueba). No sustituyen la prueba física en el Jetson.

| Prueba | Resultado |
|---|---|
| `python3 -m unittest discover -s tests -v` (20 pruebas: intérprete, respaldo parchado, `otro`/`ninguno`, umbral LAYA, varios colores, escala de prioridad, modo local) | OK |
| `python3 herramientas/probar_broker_sin_ros.py` (exclusión mutua con 4 clientes, FIFO, prioridad con envejecimiento, cancelación) | TODO OK |
| `herramientas/pruebas_sin_ros/prueba_cliente_laya.py` (rechazo antes de encolar, prioridad del modelo en el goal, CSV) | OK |
| `herramientas/pruebas_sin_ros/prueba_p3_sin_ros.py` (sin internet → modo texto; orden no permitida no llega al broker; tiempos hasta `MOVER_AGARRE`; `desglose_tiempos.py`) | OK |
| Filtro del broker `validar_pedido` (LAYA, respaldo, `SOLO_LAYA`, `colocar`, objeto/color fuera de inventario) | OK |
| `reparar_moveit.preparar_parametros` con las poses de `config/poses.json` | OK (límites J1..J6 correctos) |
| `resumen_item2.py --ultimos 10` con y sin revisión de video | OK |
| `bash -n` de los 14 scripts y ejecución en seco con `ros2`/`colcon` simulados | OK |
| `scripts/verificar_sin_clave.sh` detecta una clave `AQ.` de ejemplo | OK |
| `tablas_pregunta1.py` sobre `evidencias/pregunta1/practica_calma.csv` (latencia y exactitud de la práctica) | OK |
| Respaldo actual sobre las 50 frases de práctica | 50/50 (antes 30/50; ajustado con ese mismo conjunto) |

Pendiente en el Jetson: compilar, MoveIt real, agarre físico con la carpeta fusionada,
LAYA del docente, clave de Google (`probar_gemini.sh`), micrófono y las mediciones del examen.

Pruebas anteriores de `logistica_sinLaya1`: `docs/historico/RESULTADOS_PRUEBAS_sinLaya1.md`.
