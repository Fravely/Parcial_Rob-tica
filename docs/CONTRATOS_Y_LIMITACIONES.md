# Contratos y limitaciones (tras la fusión, 15-oct-2026)

## Contratos ROS 2

| Elemento | Nombre | Tipo |
|---|---|---|
| Servicio de decisión (P1) | `/interpretar_orden` (nodo `interprete_ordenes`) | `laya_ordenes_interfaces/srv/InterpretarOrden` |
| Acción de agarre (P2/P3) | `/logistica/pick_place` | `arm_broker_interfaces/action/PickPlace` |
| Acción RB-2 (deshabilitada en modo físico) | `/logistica/move_arm` | `arm_broker_interfaces/action/MoveArm` (`joint_positions`) |
| Estado de la cola | `/logistica/arm/queue_state` | `arm_broker_interfaces/msg/QueueState` |
| Lecturas reales del brazo | `/logistica/arm/measured_joint_states` | `sensor_msgs/JointState` (solo lectura) |
| Voz | `/voz/transcripcion`, `/voz/estado` | `std_msgs/String` |

Prioridad: mayor número = más urgente. LAYA: `score × 50`; respaldo y modo local: 20 / 80 / 180.
Política `prioridad`: puntaje = prioridad + espera_s / 0.2.

## Reglas que se cumplen

- Solo `interprete_ordenes` habla con la PC Windows (LAYA, HTTP `POST /v1/systemone`).
- Solo el hilo worker del broker abre `/dev/ttyUSB0` (pymycobot). MoveIt solo planifica.
- Una decisión con `permitido=False` no se envía al broker; el broker además la rechaza en su
  `goal_callback` si llegara.
- La clave de Google solo vive en `GEMINI_API_KEY` (archivo `~/.clave_gemini` fuera del repo).

## Limitaciones conocidas

- `physical_verified` es siempre `False`: no hay verificación visual del depósito; el éxito se
  confirma con el video.
- El error en mm es FK(q solicitada) vs FK(q leída); no mide la posición del cubo.
- Un cubo de un color retirado de la mesa se encola y falla en la cámara (no antes de encolar).
- La autorización sí/no de LAYA fue inestable en la práctica: umbral configurable (`UMBRAL_LAYA`).
- La transcripción mide red + modelo juntos (Google no informa su tiempo de cálculo).
