# TP0: Docker + Comunicaciones + Concurrencia

## Parte 1: Introducción a Docker

### Ejercicio N°4:

#### Requerimientos:
Modificar servidor y cliente para que ambos sistemas terminen de forma graceful al recibir la signal SIGTERM. 

Terminar la aplicación de forma graceful implica que todos los file descriptors 
(entre los que se encuentran archivos, sockets, threads y procesos) deben cerrarse correctamente antes que el thread de la aplicación principal muera. 
Loguear mensajes en el cierre de cada recurso (hint: Verificar que hace el flag -t utilizado en el comando docker compose down).

#### Solucion:
