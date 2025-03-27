import logging

from .utils import Bet, store_bets


class Lottery:


    def register_bet(self, msg):
        successfull_bets = 0
        bets = []

        for line in msg: # todo handlear mensaje final
            if line[0] == "F":
                break

            if line[0] == "B" and len(line) != 7:
                logging.error(f'action: apuesta_recibida | result: fail | cantidad: ${successfull_bets}')
                return None

            bet = Bet(line[1], line[2], line[3], line[4], line[5], line[6])
            bets.append(bet)
            successfull_bets += 1

        store_bets(bets)

        if successfull_bets == len(bets)-1:
            logging.info(f'action: apuesta_recibida | result: success | cantidad: ${successfull_bets}')

        return bets

    def receive_client_bets(self, client_sock):
        message = b""
        while True:
            chunk = client_sock.recv(80000)
            if not chunk:
                break
            message += chunk
            if b'\n' in chunk:
                break

        decoded_message = message.rstrip().decode('utf-8')
        lines = decoded_message.split("\n")
        lines = [line for line in lines if line.strip()]
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
