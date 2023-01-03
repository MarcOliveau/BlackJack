import random
import os
from objects.game import Game

def main():
    keep_playing = True
    game = Game()
    keep_playing = game.display_menu()
    while keep_playing:
        next_round = False

        game.cleanup_hands()
        game.deck.shuffle(len(game.players) + 1)
        game.distribute_cards()
        game.prompt_place_bets()
        game.distribute_cards()

        if game.dealer.blackjack(game):
            continue ## end round if dealer has blackjack

        game.preliminary_checks() ## checking blackjack or split possibility

        for player in game.players:
            for hand in player.hands:
                hand.pointer = True if hand.blackjack == False else False
                while hand.pointer == True: ## pointer indicates a playable hand
                    game.show_table()
                    hand.hit_or_stand(game.deck)

        while game.dealer.hand.score < 17:
            game.deck.deal(game.dealer.hand)
            game.show_table()

        game.find_results()
        game.show_table(dealer_shows=True)
        keep_playing = game.user_next_steps(next_round)

if __name__ == '__main__':
    main()
