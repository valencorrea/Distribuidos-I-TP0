import logging

from .utils import Bet, store_bets


class Lottery:


    def register_bet(self, msg):
        successfull_bets = 0
        bets = []
        eof = False
        response = "C" # Continue

        for line in msg: # todo handlear mensaje final
            fields = line.split(";")
            if fields[0] == "F":
                eof = True
                response = "F" # Finish
                break

            if fields[0] == "B" and len(fields) != 7:
                logging.error(f'action: apuesta_recibida | result: fail | cantidad: {successfull_bets}')
                store_bets(bets)
                return None

            bet = Bet(fields[1], fields[2], fields[3], fields[4], fields[5], fields[6])
            bets.append(bet)
            successfull_bets += 1

        store_bets(bets)

        if eof:
            comparison = len(msg) - 1
        else:
            comparison = len(msg)

        if successfull_bets == comparison:
            logging.info(f'action: apuesta_recibida | result: success | cantidad: {successfull_bets}')

        return response

    def receive_client_bets(self, client_sock):
        logging.info('action: receive_client_bets | result: in_progress')
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
