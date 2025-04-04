# TP0: Docker + Comunicaciones + Concurrencia

## Reentrega

#### A corregir
1. Falta close de client sockets en "happy path" y cuando se ejecuta el SIGTERM
2. No haces lock para el store_bets en "happy path" AUNQUE lo tenés ahí disponible
3. No manejas correctamente el corte de paquetes con \n en el server: puede ser que leas un paquete y parte del siguiente que va a quedar corrupto (receive_client_bets)
4. Usas threads pero no explicas por qué está bien utilizarlos en este caso de uso para python

#### Cambios realizados
1a. Se agrega el cierre del socket con el cual se este comunicando en ese momento el servidor en ese momento, inmediatamente despues de haberle enviado los documentos ganadores del sorteo.

1b. Se agrega un lockeo para el diccionario de clientes dentro de exit_gracefully para poder cerrar cada socket addres en caso de que se ejecute SIGTERM.

2. Si bien se habia agregado una variable en servidor self._bets_lock y en register_bet se utilizaba en una de las invocaciones a store_bets, 
se agrego tambien el lock para cuando se hace la ultima invocacion al final del bucle ya que alli no se estaba realizando.

3. Se edita la logica de la funcion receive_client_bets. Se crea el diccionario self.msg_buffer en donde vamos a ir almacenando para cada cliente, los mensajes que no llegamos a recibir en su totalidad.
Es decir, si leemos 1,2,3\n4 vamos a almacenar unicamente 4 y de esta manera reservarlo para cuando en el futuro llegue el resto de su contenido. Se agregan lineas de log para verificar funcionamiento.
Exclusivamente para fines de testint se cambia el valor de lectura del server a 10 bytes en client_sock.recv(10), y por simplicidad vamos a utilizar un unico cliente.

Podemos ver que como resultado se obtiene:

![](readme-images/img-1.png)

en donde la primer linea se lee en 4 chunks, y ademas se lee el id de mensaje 'B' de la segunda. Como resultado vemos que en esta iteracion se obtiene la primer linea en su totalidad y reservamos B en el buffer.

Luego vemos:

![](readme-images/img-2.png)

Podemos notar que el chunk inicia con un ';' lo cual tiene sentido porque es el que continuaba el 'B' ya enviado. Vemos que se envian todos los datos de la segunda linea y en el ultimo chunk tambien se envia 'B;1;Name;' de la tercera. Registramos esta segunda linea y guardamos lo mencionado de la 3.

![](readme-images/img-3.png)

Recibimos nuevos chunks y esta vez alcanza a completar una linea entera. Se registra la linea y el buffer aguarda ahora vacio.

4. Se utilizaron threads en este caso de uso para poder manejar multiples conexiones de clientes sin que nos quede bloqueado el servidor. 
Dada la naturaleza del problema que permite que la cantidad de clientes sea configurable al correr nuestro generar-compose.sh, debemos 
hacerlo extensible a que a su vez cada uno de ellos pueda manejarse de manera independiente. El usar threads permitio la creacion de un 
hilo para cada uno de ellos, lo cual nos garantiza que el servidor pueda antender a varios y manejar estas conexiones de manera concurrente. 
Por el contrario, de otra manera este se bloquearia a la espera de la respuesta del cliente actual.
En mi codigo se tiene un hilo principal que es el encargado de ir aceptando y handleando nuevas conexiones, y luego los hilos secundarios 
son los que van a ir resolviendo las tareas asociadas a su respectivo cliente.




