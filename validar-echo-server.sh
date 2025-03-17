#!/bin/bash

MESSAGE="Hello, server!"

# Obtengo el puerto del server del archivo de config
SERVER_PORT=$(awk -F " = " '/SERVER_PORT/ {print $2}' ./server/config.ini)
SERVER_IP=$(awk -F " = " '/SERVER_IP/ {print $2}' ./server/config.ini)

# Conecto el contenedor server a la red testing_net
docker network connect testing_net server

# Uso netcat para enviar mensaje al server y guardo respuesta
RESPONSE=$(echo "$MESSAGE" | nc $SERVER_IP $SERVER_PORT)

# Valido resultado
if [[ "$RESPONSE" == "$MESSAGE" ]]; then
  echo "action: test_echo_server | result: success"
else
  echo "action: test_echo_server | result: fail"
fi

# Finalizo conexion
docker network disconnect testing_net server
