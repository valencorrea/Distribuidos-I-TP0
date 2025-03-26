import logging

from .utils import Bet, store_bets


class Lottery:


    def register_bet(self, msg):
        if msg[0] != "B":
            return None
        bet = Bet(msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
        store_bets([bet])
        logging.info(f'action: apuesta_almacenada | result: success | dni: {msg[4]} | numero: {msg[6]}')
        return bet

    def receive_client_bet(self, client_sock):
        message = b""
        while True: # todo leer justo lo que me piden
            chunk = client_sock.recv(1024)
            if not chunk:
                break
            message += chunk
            if b'\n' in chunk:
                break
        return message.rstrip().decode('utf-8').split(";")

    def send_message(self, client_sock, message):
        try:
            total_bytes = len(message.encode('utf-8'))
            sent = 0

            while sent < total_bytes:
                n = client_sock.send(message.encode('utf-8')[sent:])
                sent += n
        except Exception as e:
            logging.error(f"action: send_message | result: fail | error: {e}")
