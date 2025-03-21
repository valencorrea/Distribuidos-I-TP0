FROM alpine:latest

# Instalo netcat en nueva imagen
RUN apk add netcat-openbsd

# Copio en el mismo directorio el archivo
COPY ./validar-echo-server.sh /

# Copio archivo de configuracion
COPY server/config.ini /server/config.ini

# Doy permisos de ejecucion
RUN chmod +x validar-echo-server.sh

ENTRYPOINT ["/validar-echo-server.sh"]