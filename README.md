# TP0: Docker + Comunicaciones + Concurrencia

## Parte 2: Repaso de Comunicaciones

### Ejercicio N°6:
Las secciones de repaso del trabajo práctico plantean un caso de uso denominado Lotería Nacional. 
Para la resolución de las mismas deberá utilizarse como base el código fuente provisto en la primera parte, con las modificaciones agregadas en el ejercicio 4.

#### Requerimientos:
Modificar los clientes para que envíen varias apuestas a la vez (modalidad conocida como procesamiento por chunks o batchs). 
Los batchs permiten que el cliente registre varias apuestas en una misma consulta, acortando tiempos de transmisión y procesamiento.

La información de cada agencia será simulada por la ingesta de su archivo numerado correspondiente, provisto por la cátedra dentro de .data/datasets.zip. 
Los archivos deberán ser inyectados en los containers correspondientes y persistido por fuera de la imagen (hint: docker volumes), manteniendo la 
convencion de que el cliente N utilizara el archivo de apuestas .data/agency-{N}.csv .

En el servidor, si todas las apuestas del batch fueron procesadas correctamente, imprimir por log: 
`action: apuesta_recibida | result: success | cantidad: ${CANTIDAD_DE_APUESTAS}`. 
En caso de detectar un error con alguna de las apuestas, debe responder con un código de error a elección e imprimir: 
`action: apuesta_recibida | result: fail | cantidad: ${CANTIDAD_DE_APUESTAS}`.

La cantidad máxima de apuestas dentro de cada batch debe ser configurable desde config.yaml. 
Respetar la clave batch: maxAmount, pero modificar el valor por defecto de modo tal que los paquetes no excedan los 8kB.

Por su parte, el servidor deberá responder con éxito solamente si todas las apuestas del batch fueron procesadas correctamente.


#### Solucion:

Se agrega a la funcion doBets la idea de que continue incluyendo lineas al batch actual a enviar, siempre y cuando el indice actual de la linea que se este leyendo en ese momento sea menos a c.config.BatchMaxAmount. En el caso de que llegue a este tope, o bien al final del archivo, se envia el mensaje al servidor. Nuevamente aqui se sigue manteniendo el protocolo del ejercicio anterior en donde los mensajes inician con un B (bets). Para indicar que se esta al final del archivo, el cliente enviara a su vez un 'F;n', en donde n representa su numero de agencia. Cuando el servidor recibe este mensaje sabe que no habra mas apuestas de la misma.

En caso de que todas las apuestas hayan llegado correctamente, se mantiene el protocolo de que el servidor conteste con el valor 'S'
