# Cambios de esta copia

- Se conserva el broker de la carpeta de origen y su worker único.
- Se incorpora un cliente PickPlace con interpretación local explícita, sin HTTP ni LAYA.
- La prioridad se obtiene de urgencia local: 1, 2 o 3, con envejecimiento del broker.
- Se utiliza la imagen completa con los HSV del notebook 5 y área mayor a 1000.
- Las cuatro poses y depósito son las proporcionadas por el usuario.
- Se conservan IK y planificación MoveIt2; el worker reproduce el plan por pymycobot.
- Se usa escaneo como paso de elevación, según notebook 5.
- Se eliminan del flujo físico los requisitos de regiones, montaje_validado,
  comprobación previa del modelo, desplazamientos nuevos de 30 mm y verificación final.
- Se mantienen manejo de errores, cancelación, exclusión del puerto y esperas de motores.
- No se acredita visualmente el éxito: physical_verified permanece en false.
- Se separan acción y tópicos del broker bajo /sin_laya; MoveIt usa sus servicios habituales.
- Los paquetes LAYA quedan excluidos mediante COLCON_IGNORE, conservando su código.
- Se incluyen instrucciones para seis terminales: MoveIt, broker y cuatro clientes.

No se modificó la carpeta de origen. No se abrió el puerto del robot, no se usó la cámara
del Jetson y no se detuvieron los procesos del otro grupo.
