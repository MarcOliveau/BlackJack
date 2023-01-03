from objects.game import Game
from objects.player import Player
from objects.deck import Card
from objects.hand import Hand
import unittest

class TestObjects(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player_names = ['jhon','laura','bob', 'billy']
        for name in self.player_names:
            self.game.add_player(name)
        self.game.deck.shuffle(1)
        for i in range(10):
            self.game.distribute_cards(display=False)
        self.hand = self.game.players[0].hands[0]
        self.test_cards = [Card('a','a',1), Card('b','b',2), Card('c','c',3)]

    def test_add_player(self):
        test_player = Player('SEB', 1000)
        self.game.add_player('sEb 222')
        self.assertEqual(self.game.players[-1].name, test_player.name)
        self.assertEqual(self.game.players[-1].cash, test_player.cash)
        self.assertEqual(len(self.game.players), 5)

    def test_remove_player(self):
        self.game.attempt_remove_player('LAURA')
        self.assertEqual(len(self.game.players), 3)
        self.assertFalse(self.game.attempt_remove_player('idontexist'))

    def test_add_funds(self):
        self.game.add_funds('JHON',100)
        self.assertEqual(self.game.players[0].cash, 1100)

    def test_get_names(self):
        self.assertEqual(self.game.get_names(), self.player_names)

    def test_get_player(self):
        self.assertEqual(self.game.get_player('LaUrA 1'), self.game.players[1])

    def test_distribute_cards(self):
        for player in self.game.players:
            self.assertEqual(len(player.hands[0].cards), 10)
        self.assertEqual(len(self.game.dealer.hand.cards), 10)

    def test_cleanup_hands(self):
        self.game.cleanup_hands()
        for player in self.game.players:
            self.assertEqual(len(player.hands[0].cards), 0)
        self.assertEqual(len(self.game.dealer.hand.cards), 0)

    def test_place_bet(self):
        bet_sizes = [10, 20, 30, 40]
        for bet, player in enumerate(self.game.players):
            player.place_bet(bet_sizes[bet])
            self.assertEqual(player.cash, 1000 - bet_sizes[bet])

    def test_split_hand(self):
        self.hand.cards = [Card('','',1), Card('','',1)]
        self.hand.split_hand(self.game.deck)
        self.assertEqual(len(self.game.players[0].hands),2)
        self.assertEqual(len(self.hand.cards),2)
        self.assertEqual(len(self.game.players[0].hands[1].cards),2)
        self.assertEqual(self.game.players[0].hands[0].bet, self.hand.bet)

    def test_player_blackjack(self):
        self.hand.cards = [Card('','',10), Card('','',11)]
        self.hand.bet = 100
        self.game.players[0].cash = 900
        self.game.players[0].check_blackjack(self.hand)
        self.assertTrue(self.hand.blackjack)

    def test_find_results_simple(self):
        self.game.dealer.hand.score = 18
        scores = [17,18,19,21]
        final_cash = [990, 1000, 1010, 1005]
        for i,player in enumerate(self.game.players):
            player.hands[0].bet = 10
            player.hands[0].score = scores[i]
            player.cash = 990
        self.game.find_results()
        for i, cash in enumerate(final_cash):
            self.assertEqual(self.game.players[i].cash, cash)

    def test_find_results_blackjack_tie(self):
        self.game.dealer.hand.score = 21
        self.game.players[0].cash = 900
        self.hand.bet = 100
        self.hand.score = 21
        self.game.find_results()
        self.assertEqual(self.game.players[0].cash,1000)

    def test_find_results_split_deck(self):
        self.game.dealer.hand.score = 17
        scores = [(10,20),(20,20),(10,10),(17,17)]
        final_cash = [1000, 1020, 980, 1000]
        for i, player in enumerate(self.game.players):
            player.cash = 980 ## two bets of 10 as deck is split
            player.hands.append(Hand(player))
            for j, hand in enumerate(player.hands):
                hand.score = scores[i][j]
                hand.bet = 10
        self.game.find_results()
        for i, cash in enumerate(final_cash):
            self.assertEqual(self.game.players[i].cash, cash)

    def test_show_hand(self):
        self.hand.cards = self.test_cards
        self.assertEqual(self.hand.show_hand(), 'aa, bb, cc')

    def test_update_score(self):
        self.hand.cards = self.test_cards
        self.hand.update_score()
        self.assertEqual(self.hand.score, 6)
        self.hand.cards = [Card('','A',11),Card('','A',11), Card('','A',11)]
        self.hand.update_score()
        self.assertEqual(self.hand.score, 13)

    def test_hit(self):
        self.hand.cards = self.test_cards
        self.game.deck.shuffle(2)
        self.hand.hit(self.game.deck)
        self.assertEqual(len(self.hand.cards), 4)
        self.assertEqual(len(self.game.deck.cards), 103)

    def test_deal(self):
        self.game.deck.cards = self.test_cards
        self.hand.cards = self.test_cards
        self.game.deck.deal(self.hand, True)
        self.game.deck.deal(self.hand, True)
        self.game.deck.deal(self.hand, True)
        self.assertEqual(len(self.hand.cards),6)
        self.assertEqual(len(self.game.deck.cards),0)
        self.assertEqual(self.hand.score,12)

if __name__ == '__main__':
    unittest.main()
