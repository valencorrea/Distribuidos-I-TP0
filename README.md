# TP0: Docker + Comunicaciones + Concurrencia

## Parte 1: Introducción a Docker

### Ejercicio N°3:

#### Requerimientos:
Crear un script de bash `validar-echo-server.sh` que permita verificar el correcto funcionamiento del servidor utilizando el comando `netcat` para interactuar con el mismo. 
Dado que el servidor es un echo server, se debe enviar un mensaje al servidor y esperar recibir el mismo mensaje enviado.

En caso de que la validación sea exitosa imprimir: `action: test_echo_server | result: success`, de lo contrario imprimir:`action: test_echo_server | result: fail`.

El script deberá ubicarse en la raíz del proyecto. Netcat no debe ser instalado en la máquina _host_ y no se pueden exponer puertos del servidor para realizar la comunicación (hint: `docker network`). `



#### Solucion:

Se agrega el target `docker-netcat` al Makefile. Este hace un build de la imagen `netcat:latest` y luego corre un contenedor, el cual se conecta a `testing_net`.
La imagen se asocia a un Dockerfile que levanta una imagen `alpine`, elegida por su pequeño tamaño. En el archivo bash `validar-echo-server.sh` que se invoca alli se obtienen las variables necesarias para la comunicacion del server desde su archivo de configuracion `config.sh`.