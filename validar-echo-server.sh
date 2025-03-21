#!/bin/sh

MESSAGE="Hello, server!"

# Obtengo el puerto del server del archivo de config
SERVER_PORT=$(awk -F " = " '/SERVER_PORT/ {print $2}' ./server/config.ini)

# Defino variables de netcat
IMAGE_NAME="netcat:latest"
CONTAINER_NAME="netcat-container"

# Buildeo imagen de netcat si no existe
if ! docker images | grep -q "$IMAGE_NAME"; then
  docker build -f ./Dockerfile -t "$IMAGE_NAME" .
fi

# Me conecto a la red testing_net y luego ejecuto en una shell netcat para enviar mensaje al server y guardarme su respuesta
RESPONSE=$(docker run --rm --network tp0_testing_net --name "$CONTAINER_NAME" "$IMAGE_NAME" sh -c "
  echo \"$MESSAGE\" | nc -w 2 server $SERVER_PORT
")

# Valido resultado
if [ "$RESPONSE" = "$MESSAGE" ]; then
  echo "action: test_echo_server | result: success"
else
  echo "action: test_echo_server | result: fail"
fi
