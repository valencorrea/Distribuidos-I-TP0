# TP0: Docker + Comunicaciones + Concurrencia

## Parte 1: Introducción a Docker

### Ejercicio N°2:

#### Requerimientos:
Modificar el cliente y el servidor para lograr que realizar cambios en el archivo de configuración no requiera reconstruír las imágenes de Docker para que los mismos sean efectivos. La configuración a través del archivo correspondiente (config.ini y config.yaml, dependiendo de la aplicación) debe ser inyectada en el container y persistida por fuera de la imagen (hint: docker volumes).



#### Solucion:

Se edita el script para agregar `volumes` al archivo `docker-compose-dev.yaml` y que la configuración ahora se persista por fuera de la imagen.
