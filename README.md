# TP0: Docker + Comunicaciones + Concurrencia

## Parte 1: Introducción a Docker

### Ejercicio N°3:

#### Requerimientos:
Crear un script de bash `validar-echo-server.sh` que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. 
Dado que el servidor es un echo server, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado.

En caso de que la validación sea exitosa imprimir: `action: test_echo_server | result: success`, de lo contrario imprimir:`action: test_echo_server | result: fail`.

El script deberá ubicarse en la raíz del proyecto. Netcat no debe ser instalado en la máquina _host_ y no se pueden exponer puertos del servidor para realizar la comunicación (hint: `docker network`). `



#### Solucion:
Se crea un Dockerfile a partir de una imagen liviana de alpine en donde se instala netcat. Luego desde el script `validar-echo-server.sh` se toma el valor de la ip del server desde su archivo de configuración, se buildea la imagen mencionada si es que aun no existe y se procede a conectarse a la red del server y establecer su comunicación.