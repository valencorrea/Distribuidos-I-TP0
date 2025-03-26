from common.utils import store_bets, Bet


class Lottery:


    def register_bet(self, msg):
        if msg[0] != "BET":
            return None
        bet = Bet(msg[1], msg[2], msg[3], msg[4], msg[5], msg[6])
        store_bets([bet])
        logging.info(f'action: apuesta_almacenada | result: success | dni: {msg[4]} | numero: {msg[6]}')
        return bet