class Hand:
    def __init__(self, player):
        self.player = player
        self.cards = []
        self.score = 0
        self.bet = 0
        self.blackjack = False
        self.pointer = False
        self.hand_type = None


    def show_hand(self, dealer_shows=None):
        '''Display the hand to terminal UI, with properties'''
        output = ""
        if dealer_shows == False:
            output += f"{self.cards[0].show()}"
            return output
        else:
            for card in self.cards:
                output += f"{card.show()}, "
            return output[:-2]

    def update_score(self):
        '''Updates the score of the hand, called when new cards are added to deck'''
        self.score = 0
        for card in self.cards:
            self.score += card.card_value
        if self.score > 21:
            self.check_for_aces()

    def check_for_aces(self):
        '''Updates the card value of Aces if the hand goes bust and hand contains an A'''
        for card in self.cards:
            if card.card == "A" and card.card_value == 11:
                card.card_value = 1
                self.update_score()
                break

    def prompt_check_split(self, deck):
        '''Checks if the hand can be split, if so allow user to split hand'''
        if self.cards[0].card == self.cards[1].card:
            split_choice = input(f"{self.player.name} can split, type '1' to split: ")
            if split_choice == '1':
                self.split_hand(deck)
            else:
                return

    def split_hand(self, deck):
        self.player.hands.append(Hand(self.player))
        split_card = self.cards[1]
        self.player.hands[-1].cards.append(split_card)
        self.player.hands[-1].bet = self.bet
        self.player.cash -= self.player.hands[-1].bet
        self.cards.remove(split_card)
        deck.deal(self)
        deck.deal(self.player.hands[-1])

    def hit_or_stand(self, deck):
        '''Allow player to either pick cards or stand'''
        hit_choice = input(f"{self.player.name}, hit (1) or stand (0)? ")
        if hit_choice == '0':
            self.pointer = False
        elif hit_choice == '1':
            self.hit(deck)
        else:
            self.hit_or_stand(deck)

    def hit(self, deck):
        deck.deal(self)
        if self.score == 21:
            self.hand_type = "BLACKJACK"
            self.pointer = False
            self.blackjack = True
        elif self.score > 21:
            self.hand_type = "BUST"
            self.pointer = False
