FROM alpine:latest

RUN which bash

# Instalo netcat en nueva imagen
RUN apk add netcat-openbsd

# Copio en el mismo directorio el archivo
COPY ./validar-echo-server.sh /

RUN apk add --no-cache bash

# Copio archivo de configuracion
COPY server/config.ini /server/config.ini

# Doy permisos de ejecucion
RUN chmod +x validar-echo-server.sh

ENTRYPOINT ["/bin/bash", "/validar-echo-server.sh"]
