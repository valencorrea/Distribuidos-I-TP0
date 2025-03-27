import socket
import logging
import signal

from .protocol import Lottery


class Server:

    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(('', port))
        self._server_socket.listen(listen_backlog)

        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self._continue = True

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

        while self._continue:
            client_sock = self.__accept_new_connection()

            if client_sock:
                self.__handle_client_connection(client_sock)

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

                response = self.lottery.register_bet(msg)
                if response:
                    if response == "F":
                        self.lottery.send_message(client_sock, "S\n")
                        break
                else:
                    self.lottery.send_message(client_sock, "E\n")


        except OSError as e:
            logging.error("action: receive_message | result: fail | error: {e}")
        finally:
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
