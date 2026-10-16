# logistica_sinLaya — prueba física del ítem 2

Copia independiente de `logistica`. Conserva su broker RB-2, las políticas FIFO/prioridad,
la cola y el único worker que controla el brazo. No se conecta a LAYA: interpreta el texto
con reglas locales. Las dependencias de LAYA quedan conservadas, pero excluidas de colcon.

La camara toma una imagen nueva cuando le toca ejecutar el pedido, despues de ir a escaneo.
Clasifica los colores dentro de cuatro regiones fijas de la imagen y selecciona las
coordenadas de la region donde aparece el color solicitado. Los colores son intercambiables;
los cuatro lugares fisicos y el encuadre de la camara deben mantenerse. No busca posiciones
libres fuera de esos cuatro lugares. No se comprueba visualmente el deposito.

La correspondencia fue corregida segun los movimientos observados por el equipo:
superior izquierda = antigua pose amarilla; inferior izquierda = antigua pose roja;
inferior derecha = antigua pose verde. Superior derecha = antigua pose azul por descarte,
pendiente de confirmar fisicamente. Los nombres antiguos solo identifican coordenadas, no colores obligatorios.
Las coordenadas estan en `config/poses_sin_laya.json`, dentro de `posiciones_recogida`.
Los nombres de los lugares no dependen del color que se coloque despues.

**MoveIt2 sigue siendo necesario** para FK del modelo, IK y planificación del ítem 2.
La reproducción física de los puntos del plan y la pinza usan pymycobot, dentro del worker.
No hay ejecución directa alternativa si falla MoveIt.
El modelo de este Jetson tiene marco raíz `dummy`: `moveit_marco: dummy` en
`config/broker_sin_laya.yaml` hace que FK e IK usen ese marco directamente.
Este cambio no altera las poses articulares enseñadas.

## 1. Subir al Jetson

Hazlo desde JupyterLab en **172.51.1.18:8888**. Los cuatro integrantes pueden usar sus
computadoras para abrir una terminal cada uno dentro del mismo Jupyter del Jetson.
No necesitan instalar Linux en sus computadoras.

Sube `logistica_sinLaya.zip` a la carpeta de inicio de Jupyter, correspondiente a
`/home/jetson`. Abre una terminal de Jupyter y ejecuta:

```bash
cd ~
unzip logistica_sinLaya.zip
cd ~/logistica_sinLaya
bash scripts/compilar.sh
```

La carpeta del ZIP debe extraerse como `/home/jetson/logistica_sinLaya`.
Compila únicamente `arm_broker_interfaces` y `arm_broker`.
El Jetson usa ROS 2 Humble, OpenCV, numpy, pymycobot y el paquete `jetcobot_moveit`
de la instalación con la que trabajaron. No es necesario instalar LAYA.

## 2. Iniciar los dos procesos del sistema

Ejecuta esta parte cuando sea el turno de tu grupo y el brazo/cámara estén libres.
El otro grupo debe cerrar sus propios programas al acabar; no cierres procesos ajenos.
Se necesita un solo MoveIt para esta prueba, un solo broker y ningún notebook
controlando a la vez el puerto /dev/ttyUSB0.

**Terminal A — MoveIt, solo planificación:**

```bash
cd ~/logistica_sinLaya
bash scripts/moveit.sh
```

Déjala abierta. Si ya hay un MoveIt de esta misma sesión de pruebas iniciado con ese
comando, conserva esa terminal y no abras un segundo proceso.

**Preparación local de MoveIt, una sola vez:** mientras la terminal A sigue abierta,
ejecuta en otra terminal:

```bash
cd ~/logistica_sinLaya
source scripts/entorno.sh
python3 reparar_moveit.py
```

Cuando indique `CONFIGURACION LOCAL LISTA`, pulsa Ctrl+C en la terminal A y vuelve a
ejecutar `bash scripts/moveit.sh`. Ahora usa `config/moveit_sin_laya.yaml`.
En los arranques siguientes el script carga automáticamente esa configuración.

El URDF observado en este Jetson limita J2, J3, J4 y J6 a aproximadamente ±90 grados.
El reparador usa los [límites documentados por Yahboom](https://www.yahboom.net/study/JetCobot/14909/)
intersectados con los del broker: cada rango queda dentro de ambos. En particular,
J2 admite ±135°, J3 aproximadamente ±144,96° y J4 ±145°. Conserva geometría,
cinemática, colisiones y límites de velocidad. Activa los límites de posición en el
URDF local y en los parámetros de MoveIt; desactiva la ejecución de trayectorias por
MoveIt. La ejecución física sigue a cargo del worker.

El reparador guarda un respaldo dentro de `config/respaldo_moveit_<fecha>/` y no cambia
archivos de `/opt/ros`. Debe ejecutarse con `/move_group` abierto porque toma sus
parámetros reales. No mueve el brazo ni abre el puerto serie.

**Terminal B — broker:**

```bash
cd ~/logistica_sinLaya
bash scripts/broker.sh
```

Déjala abierta. Debe mostrar `arm_broker listo`, política `prioridad` y modo `fisico`.
El broker espera pedidos; arrancarlo no envía movimientos al brazo. Cada script configura
automáticamente ROS_DOMAIN_ID=72 y carga esta copia del proyecto.

Los scripts se ejecutan con `bash`; no requieren `chmod`.

## 3. Abrir los cuatro clientes

Cada integrante abre **su propia terminal de Jupyter**, sin cerrar A ni B.
Los nombres pueden cambiarse, pero deben ser distintos.

| Integrante | Comandos |
|---|---|
| 1 | `cd ~/logistica_sinLaya` y luego `bash scripts/cliente.sh integrante1` |
| 2 | `cd ~/logistica_sinLaya` y luego `bash scripts/cliente.sh integrante2` |
| 3 | `cd ~/logistica_sinLaya` y luego `bash scripts/cliente.sh integrante3` |
| 4 | `cd ~/logistica_sinLaya` y luego `bash scripts/cliente.sh integrante4` |

Aparecerá un prompt como `integrante1>`. Escriban estas órdenes y presionen Enter
aproximadamente al mismo tiempo:

| Integrante | Texto que debe escribir |
|---|---|
| 1 | recoge el cubo amarillo |
| 2 | recoge el cubo azul urgente |
| 3 | recoge el cubo verde sin prisa |
| 4 | recoge el cubo rojo |

También se puede enviar una sola orden sin entrar al modo interactivo:

```bash
bash scripts/cliente.sh integrante1 "recoge el cubo amarillo"
```

**Prioridad local:** urgente/ahora/rápido = 3; normal = 2;
sin prisa/cuando puedas = 1. La cola conserva envejecimiento:
prioridad efectiva = prioridad + espera / 8 segundos.
El pedido que ya empezó termina primero; un urgente no interrumpe un agarre.
Entre los pendientes, se escoge la mayor prioridad efectiva; empate por llegada.
Por eso no hay un orden de colores garantizado si envían casi simultáneamente.

Un pedido corresponde a **un cubo**. Los cuatro pedidos de la primera ronda deben
pedir colores distintos. Para repetir, repongan los cubos en cualquiera de las cuatro posiciones
cuando la ronda haya terminado y el brazo esté en espera. Mantengan libre el punto
de descarga o usen el recipiente previsto: los cuatro comparten la misma pose.

## 4. Qué debe pasar con cada pedido

1. El cliente convierte el texto en color, objeto, acción, destino y prioridad.
   La fuente registrada es `LOCAL_SIN_LAYA`; no hay llamada HTTP ni modelo.
2. Envía una acción `/sin_laya/pick_place`. El broker la coloca en la cola.
3. El único worker toma el siguiente pedido según la política.
4. Planifica con MoveIt y mueve el brazo a la pose de escaneo.
5. Captura una imagen, localiza el color solicitado y selecciona la pose del lugar detectado.
6. Abre la pinza a 100, planifica y baja a la pose del lugar detectado.
7. Cierra a 15, levanta hacia escaneo y se traslada a la pose de depósito.
8. Abre a 100 y vuelve a escaneo; termina ese pedido y atiende el siguiente.

Velocidad del brazo: **35**. Velocidad de pinza: **45**.
Tolerancia final: **2 grados por articulación**, con el motor detenido en dos lecturas
consecutivas. Se ajustó tras el fallo observado de 1,3 grados en escaneo con el umbral
anterior de 1 grado. Es un umbral de llegada; no modifica las poses solicitadas.
No se agrega una aproximación de 30 mm ni una pose nueva inventada.

Si no se ve el color, ese pedido falla y la cola continúa.
Si hay un fallo de hardware o se interrumpe el ciclo con un cubo posiblemente sujeto,
el broker detiene la atención física; informa la causa en su terminal.
Esto es manejo de errores de ejecución, no una ronda previa de comprobaciones.

Las frases prohibidas, negativas, sin color o con varios colores se rechazan antes
de enviar movimiento. Ejemplos: `lanza el cubo rojo`, `no recojas el cubo azul`.
Para terminar un cliente inactivo, escribe `salir`.
Ctrl+C en un cliente con pedido activo solicita cancelación; no abre la pinza.

## 5. Ver la cola y los resultados

Opcional, en otra terminal:

```bash
cd ~/logistica_sinLaya
bash scripts/ver_cola.sh
```

La terminal de cada integrante muestra estados, posición en cola, resultado,
tiempo de espera y tiempo de ejecución. Los registros de esta copia están en:

- `evidencias/sin_laya/intentos.csv`: cliente, prioridad, tiempos y resultado del ciclo.
- `evidencias/sin_laya/<goal_id>/intento.json`: etapas, planes y lecturas articulares.
- `evidencias/sin_laya/<goal_id>/color.png`: captura usada para reconocer el color.
- `evidencias/sin_laya/rechazos.csv`: rechazos producidos por el broker.

Para guardar un bag, inicia antes de mandar las órdenes:

```bash
cd ~/logistica_sinLaya
bash scripts/grabar.sh
```

Al terminar la ronda, Ctrl+C en la grabación. El bag queda en `evidencias/sin_laya`.
La captura PNG se guarda por separado; el video de la prueba se graba por separado.

`success=True` significa que terminó el ciclo de comandos. Como se omitió la
comprobación visual final, `physical_verified=False` es normal: no significa por sí
solo que falló el agarre. Ustedes observan si el cubo llegó. El error en mm registrado
es la desviación de las articulaciones leídas respecto a las solicitadas, expresada
con FK RB-2; no mide directamente la posición del cubo.

Esta es una prueba funcional sin LAYA; no acredita la integración con LAYA ni sustituye
los diez intentos físicos y evidencias que pide el examen. No se probó el movimiento
real desde Windows.

## 6. Finalizar

Esperen a que los cuatro clientes indiquen que terminó su pedido.
Escriban `salir` en los clientes y luego Ctrl+C en broker y MoveIt.
El brazo permanece en escaneo; cerrar el programa no lo envía a home automáticamente.

## Archivos activos

- `config/poses_sin_laya.json`: las cuatro poses, depósito, escaneo y pinza.
- `config/broker_sin_laya.yaml`: prioridad, inventario y MoveIt.
- `src/arm_broker/arm_broker/broker.py`: broker original adaptado a esta secuencia.
- `src/arm_broker/arm_broker/orden_local.py`: reglas de texto sin LAYA.
- `src/arm_broker/arm_broker/cliente_sin_laya.py`: cliente para cada integrante.
- `scripts/`: los comandos de esta guía.

Los demás manuales y plantillas se conservaron como referencia de la carpeta original.
Para **esta variante**, sigue este README y los scripts de arriba; no los procedimientos
antiguos de regiones, previsualización o LAYA. Los directorios generados build/install/log,
cachés y la copia anidada logistica no se copiaron; se genera una instalación propia.


### Recuperar un cubo sujeto tras un fallo

Detener solo el broker con Ctrl+C y mantener MoveIt abierto. No enviar pedidos durante la recuperacion. Ejecutar desde la raiz: `source scripts/entorno.sh` y `python3 recuperar_cubo.py --ejecutar`. El ultimo comando mueve el brazo: retoma escaneo, va al deposito y abre la pinza solo al completar ambos segmentos. No captura imagen ni comienza otra recogida. Si falla, no abre automaticamente la pinza. No reiniciar pedidos hasta comprobar que ya deposito el cubo. Sin `--ejecutar`, muestra ayuda y no conecta al robot.
