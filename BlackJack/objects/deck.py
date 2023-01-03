import random

class Deck:
    def __init__(self):
        self.cards = []

    def deal(self, hand, printer=False):
        '''Distributes a single card so a single hand'''
        card = self.cards[0]
        self.cards = self.cards[1:]
        hand.cards.append(card)
        hand.update_score()

    def shuffle(self, num_deck):
        '''Creates a new deck before the start of a round'''
        suits = ["♠", "♡", "♣", "♢"]
        cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        cards_values = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":1, "Q":2, "K":3}
        self.cards = []
        for suit in suits:
            for card in cards:
                for i in range(num_deck):
                    self.cards.append(Card(suit, card, cards_values[card]))
        random.shuffle(self.cards)

class Card:
    def __init__(self, suit, card, card_value):
        self.suit = suit
        self.card = card
        self.card_value = card_value

    def show(self):
        '''Display card information for terminal UI'''
        card = f"{self.card}{self.suit}"
        return card
