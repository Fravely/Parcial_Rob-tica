# Origen de los archivos, contratos y lo que falta para el examen

## Archivos recibidos (conservados en `referencia_codigos_companero/`)
- `broker.py`, `cliente.py`, `politicas.py`, `fk.py`: archivos aportados en la conversación.
- `TUTORIAL_ITEM2.md` y herramientas de prueba, carga y auditoría.
- `kinematics.py` fue creado en una interacción previa y el usuario indicó que NO es suyo.
  **No está en este ZIP ni se utiliza**.

## Cambios de integración hechos aquí
- `src/arm_broker/`: mismo algoritmo del `broker.py` recibido, con parámetro
  `publicar_joint_states:=false` por defecto y mensajes `SIMULADO`; `cliente.py`
  escribe CSV por goal. Archivos de entrada SIN modificar conservados en referencia.
- Manifiestos ROS 2 `setup.py`, `package.xml`, interfaz `MoveArm.action` y `QueueState.msg`
  reconstruidos desde `TUTORIAL_ITEM2.md` compatible con `broker.py`.
- `laya_ordenes` reutiliza `node.py` y `logic.py` del kit que se demostró en el robot,
  y el puente `orden_a_broker.py` corresponde a `joint_positions`.
- `herramientas/exportar_csv.py`, `metricas_item3.py`, `evaluar_50.py` son NUEVOS.

## NO mezclar con el otro broker de rb2_ws
| Version | action goal | prioridad | fuente de cinemática | ejecutable |
| --- | --- | --- | --- | --- |
| `logistica` (esta entrega) | `joint_positions` | MAYOR = más urgente | `fk.py` del compañero | `arm_broker broker` |
| `~/rb2_ws` observado por captura | `q_deseado` | MENOR = más urgente | `kinematics.py` externo (NO disponible) | `arm_broker arm_broker_node` |

La versión de `~/rb2_ws` no puede reconstruirse fielmente sin disponer de su fuente
original completa. **No afirmar que se completó esa variante**.

## Aún no implementado ni probado físicamente
- Servidor LAYA compartido (IP/puerto/preset docente no confirmados), nunca probado aquí.
- Visión/cámara para localizar cuatro objetos, coordenadas físicas, IK validada al agarrar,
  MoveIt2 plan, gripper y secuencia pick-and-place: **pendientes**.
- Transcriptor Google AI Studio: no implementado. Clave debe ser variable de entorno.
- La rúbrica exige `50 frases` y `5 órdenes de voz`: aún NO recibidas.
- No se ha demostrado control físico, exclusión sobre bag real o exactitud del modelo LAYA.

## LAYA no es ROS
HTTP POST a `/v1/systemone` desde SOLO `interprete_ordenes`.
El tipo `choice` clasifica acción/objeto/color, `score` prioridad, `noul`
autorización. Si falla, la respuesta viene `degradada=True`.
El análisis `resto_http_ms` no significa RTT de red puro: incluye colas,
serialización y otros tiempos del servidor.

## Seguridad de manipulación
`permitido=true` significa solo que la frase es autorizable, NO que el objeto
exista ni que el movimiento esté validado. La bandera `habilitar_movimiento`
del adaptador solo permite enviar el goal; la bandera del broker
`publicar_joint_states=true` es otro permiso independiente. Si falta pose calibrada,
se rechaza. Ningún nodo nuevo salvo el broker publica a `/joint_states`.
