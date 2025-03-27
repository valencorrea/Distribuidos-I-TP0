import socket
import logging
import signal

from .protocol import Lottery
from .utils import load_bets, has_won


class Server:

    def __init__(self, port, listen_backlog, clients_amount):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)
        self._clients = {}
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self._continue = True
        self.clients_amount = clients_amount

        self.lottery = Lottery()

    def exit_gracefully(self, signum, frame):
        self._continue = False
        logging.info('action: close_server_socket | result: in_progress')
        self._server_socket.close()
        logging.info('action: close_server_socket | result: success')


    def run(self):
        """
        Dummy Server loop

        Server that accept a new connections and establishes a
        communication with a client. After client with communucation
        finishes, servers starts to accept new connections again
        """

        # TODO: Modify this program to handle signal to graceful shutdown
        # the server

        index = 0

        while self._continue and index < self.clients_amount:
            client_sock = self.__accept_new_connection()

            if client_sock:
                self.__handle_client_connection(client_sock)
                index += 1

        all_bets = load_bets()
        winners = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }

        for bet in all_bets:
            if has_won(bet):
                documents = winners[bet.agency]

                winners[bet.agency] = documents.append(bet.document)

        for agency, sock in self._clients.items():
            winner_message = f"W;{';'.join(winners[agency])}\n"
            self.lottery.send_message(sock, winner_message)

        logging.info(f'action: sorteo | result: success')


    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            while True:
                logging.info('action: handle_client_connection | result: in_progress')
                msg = self.lottery.receive_client_bets(client_sock)
                addr = client_sock.getpeername()
                logging.info(f'action: receive_message | result: success | ip: {addr[0]} | msg: {msg}')

                eof, bets, client_id = self.lottery.register_bet(msg)
                if eof is None:
                    self.lottery.send_message(client_sock, "E\n")
                    break
                if eof is True:
                    self._clients[client_id] = client_sock # lo hago una vez cuando termine de leer el archivo
                    break
                elif bets:
                    self.lottery.send_message(client_sock, "S\n")

        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
            client_sock.close()

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info('action: accept_connections | result: in_progress')
        try:
            c, addr = self._server_socket.accept()
            logging.info(f'action: accept_connections | result: success | ip: {addr[0]}')
            return c
        except OSError as e:
            logging.error(f"action: accept_connections | result: fail | error: {e}")
            return None
