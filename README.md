# TP0: Docker + Comunicaciones + Concurrencia

## Parte 2: Repaso de Comunicaciones

### Ejercicio N°5:
Las secciones de repaso del trabajo práctico plantean un caso de uso denominado Lotería Nacional. 
Para la resolución de las mismas deberá utilizarse como base el código fuente provisto en la primera parte, con las modificaciones agregadas en el ejercicio 4.

#### Requerimientos:
Modificar la lógica de negocio tanto de los clientes como del servidor para nuestro nuevo caso de uso.

##### Cliente
Emulará a una _agencia de quiniela_ que participa del proyecto. Existen 5 agencias. 
Deberán recibir como variables de entorno los campos que representan la apuesta de una persona: nombre, apellido, DNI, nacimiento, numero apostado (en adelante 'número'). 
Ej.: `NOMBRE=Santiago Lionel`, `APELLIDO=Lorca`, `DOCUMENTO=30904465`, `NACIMIENTO=1999-03-17` y `NUMERO=7574` respectivamente.

Los campos deben enviarse al servidor para dejar registro de la apuesta. Al recibir la confirmación del servidor se debe imprimir por log: `action: apuesta_enviada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

##### Servidor
Emulará a la _central de Lotería Nacional_. Deberá recibir los campos de la cada apuesta desde los clientes y almacenar la información mediante 
la función `store_bet(...)` para control futuro de ganadores. La función `store_bet(...)` es provista por la cátedra y no podrá ser modificada por el alumno.
Al persistir se debe imprimir por log: `action: apuesta_almacenada | result: success | dni: ${DNI} | numero: ${NUMERO}`.

##### Comunicación:
Se deberá implementar un módulo de comunicación entre el cliente y el servidor donde se maneje el envío y la recepción de los paquetes, el cual se espera que contemple:
* Definición de un protocolo para el envío de los mensajes.
* Serialización de los datos.
* Correcta separación de responsabilidades entre modelo de dominio y capa de comunicación.
* Correcto empleo de sockets, incluyendo manejo de errores y evitando los fenómenos conocidos como [_short read y short write_](https://cs61.seas.harvard.edu/site/2018/FileDescriptors/).


#### Solucion:
Desde la parte del cliente se suman los nuevos campos `nombre, apellido, documento, fecha de nacimiento y numero apostado` como se solicito en el enunciado. Estos valores se sumaron al .yaml y son interpretados como variables de entorno desde el `main.go`. En el flujo se invoca a realizar una apuesta, en donde se formatea el mensaje a enviar al server y luego se envia, teniendo en cuenta la cantidad de bytes restantes por mandar. 
El protocolo que se definio aqui es:

`B,{id},{nombre},{apellido},{documento},{nacimiento},{numero}`

en donde B indica que el mensaje pertenece a una apuesta.
De no ocurrir errores, se espera la respuesta del servidor. Las posibles opciones aqui son:

`S`

equivalente a una respuesta exitosa, o bien

`E`

si ocurrio algun error en el servidor.

Desde el lado del servidor, se agrega una instancia de loteria a su estructura. Al recibir un mensaje, este valida lo lee y deserializa. Una vez obtenido el mensaje, en caso de exito crea una `Bet` y guarda la misma utilizando `store_bet(...)`.
En base al resultado de estas operaciones envia una respuesta al cliente segun lo detallado previamente.

Se puede ver el flujo de la logica ejecutando el comando de logs.