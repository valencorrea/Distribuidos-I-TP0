#!/bin/bash

MESSAGE="Hello, server!"

# Obtengo el puerto del server del archivo de config
SERVER_PORT=$(awk -F " = " '/SERVER_PORT/ {print $2}' ./server/config.ini)

# Uso netcat para enviar mensaje al server y guardo respuesta
RESPONSE=$(echo "$MESSAGE" | nc -w 2 server $SERVER_PORT)

# Valido resultado
if [[ "$RESPONSE" == "$MESSAGE" ]]; then
  echo "action: test_echo_server | result: success"
else
  echo "action: test_echo_server | result: fail"
fi
