# TP0: Docker + Comunicaciones + Concurrencia

## Parte 3:COncurrencia

### Ejercicio N°8: Concurrencia

#### Requerimientos:
Modificar el servidor para que permita aceptar conexiones y procesar mensajes en paralelo. En caso de que el alumno implemente el servidor en Python utilizando multithreading, deberán tenerse en cuenta las limitaciones propias del lenguaje.


#### Solucion:

Se agregan en el server campos para realizar luego los lockeos de escritura de secciones criticas que pueden ser accedidas por cualquiera de los clientes. A su vez se crea un thread para cada uno, y luego se espera a la finalizacion de todos ellos.

