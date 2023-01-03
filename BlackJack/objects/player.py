from objects.hand import Hand

class Player:
    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.hands = [Hand(self)]

    def check_blackjack(self, hand):
        '''Updates players hand properties and cash if the hand is a blackjack'''
        hand.update_score()
        if hand.score == 21:
            hand.hand_type = "BLACKJACK"
            hand.blackjack = True

    def clean_hand(self):
        '''Reinitialize the players hand before a round starts'''
        self.hands = [Hand(self)]

    def place_bet(self, bet_size):
        self.hands[0].bet = bet_size
        self.cash -= bet_size
