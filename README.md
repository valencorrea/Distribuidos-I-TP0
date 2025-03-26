# TP0: Docker + Comunicaciones + Concurrencia

## Parte 1: Introducción a Docker

### Ejercicio N°4:

#### Requerimientos:
Modificar servidor y cliente para que ambos sistemas terminen de forma graceful al recibir la signal SIGTERM. 

Terminar la aplicación de forma graceful implica que todos los file descriptors 
(entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. 
Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag -t utilizado en el comando docker compose down).

#### Solucion:
En lo que respecta al servidor, se da aviso a traves de signal que cuando se reciba la señal `SIGTERM` se debera invocar `exit_gracefully`. Esta lo que hace es editar la variable
que controla el loop principal y a su vez cierra el socket del server. Por otro lado tambien se ejecuta el llamado de accept del socket dentro de una 
estructura try catch ya que ante errores arroja la excepcion `OSError: [Errno 9] Bad file descriptor`.

Por otro lado, desde el cliente se crea un canal al cual tambien se le indica escuchar la syscall `SIGTERM`. En caso de recibirla se cierra la conexion abierta del cliente y finaliza el loop.

Para ejecutar el ejercicio se pueden correr los comandos `docker-sigterm-{server/client1}`.
