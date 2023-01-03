import os
import random
from objects.player import Player
from objects.dealer import Dealer
from objects.deck import Deck

class Game:
    def __init__(self):
        self.players = []
        self.dealer = Dealer()
        self.deck = Deck()

## Start of menu functionality code

    def display_menu(self):
        '''Displays users command options, and redirects user to designated function'''
        menu = True
        while menu:
            os.system("clear")
            self.show_header()
            user_input = input("command: ")
            if user_input == '1':
               self.prompt_add_player()
            elif user_input == '2':
                self.prompt_remove_player()
            elif user_input == '3':
                self.prompt_add_funds()
            elif user_input == '4': ## starts a blackajck round
                if len(self.players) < 1:
                    message = input("You need to add players, press enter to continue")
                    continue
                else:
                    return True
            elif user_input == '0': ## exits program
                return False
            else:
                continue

    def show_header(self):
        '''Prints the header of the menu'''
        print("------------------------ BLACKJACK MENU ------------------------ (type 'back' to return from command)")
        print(f"Current players: {self.get_names()}")
        print("---")
        print("add player(1), remove player(2), add funds(3), start game(4), exit game(0)")
        print("---")

    def get_names(self):
        '''Gets the list of names of current players'''
        player_names = [player.name.lower() for player in self.players]
        return player_names

    def prompt_add_player(self):
        '''Adds a new player to the game object'''
        name = input('add player name: ')
        if name == 'back':
            return
        self.add_player(name)

    def add_player(self, name):
        self.players.append(Player(name.split()[0].upper().strip(), 1000))

    def prompt_remove_player(self):
        '''Removes a player from the game'''
        while(True):
            name = input('remove player name: ')
            if name == 'back':
                return
            check = self.attempt_remove_player(name.split()[0].upper().strip())
            if check:
                break
            else:
                print(f"player not found")
                continue

    def attempt_remove_player(self, name):
        '''Checks if the user requested to remove an existing player'''
        new_players = []
        for player in self.players:
            if player.name != name:
                new_players.append(player)
        if len(new_players) == len(self.players):
            return False
        else:
            self.players = new_players
            return True

    def prompt_add_funds(self):
        '''Increase the players cash by a user specified amount'''
        while(True):
            player_name = input('choose player to add funds for: ')
            if player_name == 'back':
                return
            players = self.get_names()
            if player_name.split()[0].lower().strip() not in players:
                print('name not found')
                continue
            else:
                while(True):
                    player_funds = input('Amount of $$$ to add: ')
                    if player_funds == 'back':
                        return
                    try:
                        player_funds = float(player_funds)
                        break
                    except:
                        print("value needs to be a float")
                        continue
                self.add_funds(player_name, player_funds)
                break

    def add_funds(self, player_name, player_funds):
        player_obj = self.get_player(player_name)
        player_obj.cash += player_funds

    def get_player(self, name):
        '''Get the player object of a specified player name'''
        for player in self.players:
            if player.name == name.split()[0].upper().strip():
                return player

### End of menu functionality code

## Start of game mechanics code

    def cleanup_hands(self):
        '''Restarts all players and dealer hands before round starts'''
        for player in self.players:
            player.clean_hand()
        self.dealer.hand.cards = []

    def distribute_cards(self, display=True):
        '''Distributes all players and dealer a single card from the deck'''
        for player in self.players:
            self.deck.deal(player.hands[0])
        self.deck.deal(self.dealer.hand)
        if display:
            self.show_table()

    def prompt_place_bets(self):
        '''Allows all players to place a bet, checks that user input is valid'''
        for player in self.players:
            while(True):
                try:
                    bet_size = float(input(f"{player.name}, place a bet: "))
                    if bet_size > player.cash:
                        print("You don't have the funds for that")
                        continue
                    else:
                        break
                except:
                    print("bet needs to be a float")
                    continue
            player.place_bet(bet_size)
            self.show_table()

    def preliminary_checks(self):
        '''Checking if any hand can be split or is a blackjack'''
        for player in self.players:
            for hand in player.hands:
                hand.prompt_check_split(self.deck)
                player.check_blackjack(hand)
                self.show_table()
        self.show_table()

    def show_table(self, dealer_shows=False):
        '''Displays all players hands and dealer hand to UI'''
        os.system("clear")
        print("############# CURRENT TABLE ################")
        for player in self.players:
            print(player.name, f"- {player.cash}$")
            for num_hand, hand in enumerate(player.hands):
                pointer = "" if hand.pointer == False or hand.blackjack == True else "<------"
                results = hand.hand_type if hand.hand_type is not None else ""
                bet_display = f"Bet:{hand.bet}$" if results == "" else ""
                print(f"        Hand {num_hand + 1} - {hand.show_hand()} || Score:{hand.score} {bet_display} {results}{pointer}")
        print("DEALER")
        if dealer_shows:
            print(f"        {self.dealer.hand.show_hand()} || {self.dealer.hand.score}")
        else:
            print(f"        {self.dealer.hand.show_hand(dealer_shows)} *** || Score: {self.dealer.hand.cards[0].card_value}")
        print("#############################################")

    def find_results(self):
        '''Updates players cash and their hands properties for displaying to UI'''
        if self.dealer.hand.score == 21:
            for player in self.players:
                for hand in player.hands:
                    if hand.score != 21:
                        hand.hand_type == "LOSE"
                    else:
                        hand.hand_type == "TIE"
                        player.cash += hand.bet
        else:
            for player in self.players:
                    for hand in player.hands:
                        if hand.score == 21:
                            player.cash += hand.bet * 1.5
                        elif hand.hand_type is None:
                            if hand.score == self.dealer.hand.score:
                                player.cash += hand.bet
                                hand.hand_type = "TIE"
                            elif hand.score > self.dealer.hand.score or self.dealer.hand.score > 21:
                                player.cash += hand.bet * 2
                                hand.hand_type = "WIN"
                            else:
                                hand.hand_type = "LOSE"

    def user_next_steps(self, next_round):
        '''Redirects user to continue, go to menu, or exit game'''
        while next_round == False:
            player_choice = input("next round (1), menu(2) or exit game(0): ")
            if player_choice == '1':
                return True
            elif player_choice == '0':
                return False
            elif player_choice == '2':
                return self.display_menu()
            else:
                self.show_table(dealer_shows=True) ## bad input will return to same prompt
