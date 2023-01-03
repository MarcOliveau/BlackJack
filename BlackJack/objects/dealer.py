from objects.hand import Hand

class Dealer:
    def __init__(self):
        self.hand = Hand(self)

    def blackjack(self, game):
        '''Checks if dealer has blackjack, if so move to next round'''
        self.hand.update_score()
        if self.hand.score == 21:
            game.find_results()
            game.show_table(dealer_shows=True)
            r = input("Dealer got blackjack! press enter for next round")
            return True
