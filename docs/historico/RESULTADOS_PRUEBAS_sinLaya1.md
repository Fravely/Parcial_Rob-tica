# Pruebas de software — 14/10/2026

Resultado: 10 pruebas aprobadas con unittest; sin ROS ni hardware real.

- Cuatro clientes, incluyendo tres envíos concurrentes mientras el primero se ejecuta.
- Prioridad y un único worker para cámara, planificación y movimientos.
- Poses del usuario, velocidad 35 y pinza 100/15 a velocidad 45.
- Secuencia escaneo, recogida, escaneo, depósito y retorno a escaneo.
- Rechazo antes de encolar, cancelación en cola y continuación tras color ausente.
- Interrupción con cubo posiblemente sujeto sin abrir la pinza para el siguiente.
- Registro explícito de fuente LOCAL_SIN_LAYA y ausencia de verificación visual final.

Sintaxis Python compatible con 3.10: aprobada.
Sintaxis de los 7 scripts Bash mediante bash -n: aprobada.

No se ejecutó colcon ni ROS2 en Windows; no se abrió la cámara ni el puerto serie.
La planificación real de MoveIt y el agarre físico se ejecutan al correr en el Jetson.
No se presentan estas pruebas como diez intentos reales del examen.

Para repetir las pruebas de software (opcional):

```bash
python3 -m unittest discover -s pruebas_sin_laya -v
```

## Corrección de límites de MoveIt

Siete pruebas adicionales de software aprobadas para `reparar_moveit.py`:
intersección con límites oficiales y del broker, preservación de geometría/velocidad,
parámetros null/NaN, rechazo de poses fuera de rango, conservación de límites suaves,
rechazo de modelo incompleto y manejo de parámetros planos o anidados.
Sintaxis Python 3.10 y del script Bash generado comprobada.
La aplicación al MoveIt real queda a cargo de ejecutar el reparador en el Jetson.


Reintento final limitado: 7 pruebas con reloj y controlador simulados aprobadas. Un reenvio del mismo destino solo detenido y entre la tolerancia final y 3 grados; conserva plazo y velocidad. Se comprobaron correccion, limite de reintentos, motor en movimiento, error grande, llegada normal, cancelacion y rechazo del controlador. Pendiente prueba fisica.


Recuperacion y lectura serial: 8 pruebas simuladas aprobadas. Se comprueban respuesta transitoria, persistente, motor activo, cancelacion, plazo y apertura solo despues de ambos movimientos. Recuperacion fisica pendiente. La reconsulta no demuestra la causa del fallo original.


Lectura de angulos: seis pruebas simuladas aprobadas (valida, transitoria, persistente, valores invalidos, cancelacion, plazo). No se publica telemetria incompleta. Prueba fisica pendiente.


Recepcion SDK 3.4.6: seis pruebas simuladas aprobadas del adaptador de _read (0.5 s), preservacion de argumentos, plazos antes/durante consulta, estados invalidos y validos. No demuestra la causa fisica de los None. Diagnostico de diez lecturas preparado, pendiente en Jetson.


Correccion consolidada en broker.py: verificada directamente en memoria sin nuevos archivos de prueba. Adaptador con cadencia minima de 50 ms y recepcion de 0.5 s; todos los puntos conservados; consultas de movimiento solo al final; motor activo no aceptado como llegada; cancelacion y lecturas incompletas comprobadas; sin importaciones de auxiliares desde src. Validacion fisica pendiente.


Localizacion por lugar: detector OpenCV ejecutado sobre la foto del usuario, con cuatro posiciones correctas. Se comprobaron 24 permutaciones de color sinteticas en memoria, ausencia y duplicados. Secuencia real probada con dobles de hardware en 16 combinaciones color/lugar; captura posterior al escaneo y anterior a la apertura, y seleccion de pose por lugar. No se crearon archivos de prueba. Falta validacion fisica con colores intercambiados.
