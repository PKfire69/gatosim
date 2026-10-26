import GameState
from Deck import Deck
from Player import Player


class Game:
    """is the main loop of the game which is called by the __name__ and intializes game variables that are used throughout the game"""

    def __init__(self):
        self.deck = Deck()
        self.players = []
        self.show_rules()

    """prints a list of rules and how the game works"""

    def show_rules(self):
        print(
            "Hello, this is not only a card game but a game of chance. You will be pitted against your friend where the choices you make will effect the outcome of the game."
        )
        print(
            "Each player draws three cards from a deck of 10 characters and chooses one active character for the battle."
        )
        print(
            "You and your opponent will take turns making two options; Attack or Defend."
        )
        print(
            "Take turns until one active character reaches 0 health. The other player wins the battle."
        )

    """Sets up the game by instantiating the players and their hands"""

    def setup(self):
        self.players = [
            Player(input("Enter player one's name: ").strip()),
            Player(input("Enter player two's name: ").strip()),
        ]
        for player in self.players:
            player.draw_hand(self.deck)
        for player in self.players:
            player.choose_card()

    """Asks whether to resume the saved game. Returns True for yes"""

    def ask_resume(self):
        while True:
            choice = input("You have a saved game. Resume? (y/n): ").strip().lower()
            if choice in ("y", "n"):
                return choice == "y"
            print("Please enter y or n.")

    """ This is the main loop of the game and keeps the game running until one of the active cards is dead"""

    def play(self):
        saved = GameState.resume_game()
        if saved and self.ask_resume():
            self.players = saved
        else:
            self.setup()
            GameState.update_game(self.players[0], self.players[1])

        current, other = self.players
        while current.active_card.is_alive() and other.active_card.is_alive():
            current.take_turn(other)
            if not other.active_card.is_alive():
                current.score += 1
                print(f"\n{current.name} wins the battle!")
                GameState.clear_game()
                break
            current, other = other, current
            GameState.update_game(current, other)


if __name__ == "__main__":
    game = Game()
    game.play()