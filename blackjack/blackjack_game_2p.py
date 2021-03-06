import random
from tkinter import Tk, ttk
from PIL import ImageTk, Image

class Card:

    number_name_mapping = {
        1: "ace",
        11: "jack",
        12: "queen",
        13: "king",
    }
    card_image_path = "./assets/png/"

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        self.tk_img = ImageTk.PhotoImage(Image.open(self.get_card_image_path()))

    def get_card_image_path(self):
        return "{}{}_of_{}.png".format(self.card_image_path, self.number_name_mapping.get(self.number, self.number),
                                       self.suit)

    def __str__(self):
        return "{} of {}".format(self.number, self.suit)


class Deck:
    suits = ["diamonds", "hearts", "spades", "clubs"]
    max_number = 13

    def __init__(self):
        self.cards = []
        self.used_cards = []

        for suit in self.suits:
            for number in range(1, self.max_number + 1):
                self.cards.append(Card(number, suit))

    def give_random_card(self):
        position = random.randint(1, len(self.cards))
        chosen_card = self.cards.pop(position)
        self.used_cards.append(chosen_card)
        try:
            return chosen_card
        except IndexError:
            print("Se acabó")


class Player:
    points = 0
    table_cards = []

    def __init__(self, name):
        self.name = name


class Game:
    card_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 10, 12: 10, 13: 10}

    n_players = 2

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.ui_root = Tk()
        self.table_cards = []

    def ask_player_name(self, player_n):
        return input("¿Cual es el nombre del {}?: ".format(player_n))

    def draft_card(self):
        card = self.deck.give_random_card()
        self.table_cards.append(card)
        return card

    def count_table_cards(self):
        total = 0

        for card in self.table_cards:
            if card.number == 1 and total + self.card_values[card.number] > 21:
                total += 1
            else:
                total += self.card_values[card.number]

        return total

    def player_wants_to_continue(self):
        response = input("¿Quieres otra carta[Y/N]?")
        return response == "Y"

    def start_turn(self, player):
        self.table_cards = []
        self.deck = Deck()
        print("\nTurno de {}\n".format(player.name))

    def play(self):
        card_frame = ttk.Frame(self.ui_root, padding="30 12 30 12")
        card_frame.grid()
        number_of_cards_per_row = 5

        for card_n in range(10):
            card = self.deck.give_random_card()
            row = int(a / number_of_cards_per_row)

            ttk.Label(card_frame, image=card.tk_img).grid(column=card_n%number_of_cards_per_row, row=row)

        self.ui_root.mainloop()

        for i in range(self.n_players):
            self.players.append(Player(self.ask_player_name(i + 1)))

        user_continue = True
        winner_score = 0
        winner = None

        for player in self.players:
            self.start_turn(player)

            while not self.count_table_cards() > 21 and user_continue:
                self.draft_card()
                user_continue = self.player_wants_to_continue()

            player.points = self.count_table_cards()
            print("Tu puntuación es : {}".format(player.points))

            if player.points > 21:
                print("Perdiste")
            elif player.points > winner_score:
                winner_score = player.points
                winner = player

        print("El ganador es {} con {} puntos".format(winner.name, winner_score))


if __name__ == "__main__":
    blackjack = Game()
    blackjack.play()
