import logging

from .utils import Bet, store_bets


class Lottery:
    def __init__(self):
        self.msg_buffer = {}

    def register_bet(self, msg, bets_lock):
        successfull_bets = 0
        bets = []
        eof = False
        message_client = False
        client_id = 0

        for line in msg:
            fields = line.split(";")
            if len(fields) == 0 or fields[0] == "F":
                client_id = int(fields[1])
                eof = True
                break

            if len(fields) > 0 and fields[0] == "B" and len(fields) != 7:
                logging.error(f'action: apuesta_recibida | result: fail | cantidad: {successfull_bets}')

                with bets_lock:
                    store_bets(bets)

                return None, 0, client_id

            bet = Bet(fields[1], fields[2], fields[3], fields[4], fields[5], fields[6])
            bets.append(bet)
            successfull_bets += 1
            client_id = bet.agency

        with bets_lock:
            store_bets(bets)

        if successfull_bets == len(bets):
            message_client = True
            logging.info(f'action: apuesta_recibida | result: success | cantidad: {successfull_bets}')

        return eof, message_client, client_id

    def receive_client_bets(self, client_sock):
        logging.info('action: receive_client_bets | result: in_progress')

        if client_sock not in self.msg_buffer:
            self.msg_buffer[client_sock] = b""

        while b'\n' not in self.msg_buffer[client_sock]:
            chunk = client_sock.recv(1024)
            if not chunk:
                break
            logging.info(f"CHUNK RECIBIDO: {chunk}")
            self.msg_buffer[client_sock] += chunk

        data = self.msg_buffer[client_sock]
        lines = data.split(b'\n')
        logging.info("LINEAS COMPLETAS:")
        for line in lines[:-1]:
            logging.info(f"{line.decode()}")

        self.msg_buffer[client_sock] = lines[-1]
        logging.info(f"ALMACENO EN BUFFER: {lines[-1]}")

        lines = [line.decode('utf-8').strip() for line in lines[:-1] if line.strip()]
        return lines

    def send_message(self, client_sock, message):
        try:
            total_bytes = len(message.encode('utf-8'))
            sent = 0

            while sent < total_bytes:
                n = client_sock.send(message.encode('utf-8')[sent:])
                sent += n
        except Exception as e:
            logging.error(f"action: send_message | result: fail | error: {e}")
