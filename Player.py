from copy import deepcopy
from Cards import Card

class Player:
    """instantiates players with different attributes stated below"""

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        self.active_card = None

    def to_dict(self):
        data = {
            "playerName": self.name,
            "score": self.score,
            "hand": [card.to_dict() for card in self.hand],
            "active_card": self.hand.index(self.active_card)
            if self.active_card is not None
            else None,
        }
        return data

    def to_dict(self):
        active = None
        if self.active_card is not None:
            active = self.hand.index(self.active_card)
        return {
            "playerName": self.name,
            "score": self.score,
            "hand": [card.to_dict() for card in self.hand],
            "active_card": active,
        }

    def from_dict(data):
        player = Player(data["playerName"])
        player.score = data["score"]
        player.hand = [Card.from_dict(c) for c in data["hand"]]
        if data["active_card"] is not None:
            player.active_card = player.hand[data["active_card"]]
        return player

    """Is the string dunder method that that returns a string of the players name and their respected score """

    def __str__(self):
        return f"{self.name} (score: {self.score})"

    """is called at the beginning of the game to draw 3 cards into a players hand and sorts them alphabetically"""

    def draw_hand(self, deck, size=3):
        while len(self.hand) < size:
            self.hand.append(deck.draw_card())
        self.hand.sort(key=lambda card: card.name)

    """is a method that is called to make a player choose an active card for battle"""

    def choose_card(self):
        if not self.hand:
            raise ValueError("Draw a hand before choosing a card")
        print(f"{self.name}, choose your active character:")
        for i, card in enumerate(self.hand, start=1):
            print(f"{i}. {card}")
        valid = [str(n) for n in range(1, len(self.hand) + 1)]
        choice = input(f"Enter 1 to {len(self.hand)}: ").strip()
        while choice not in valid:
            choice = input(f"Please enter 1 to {len(self.hand)}: ").strip()
        self.active_card = self.hand[int(choice) - 1]
        print(f"{self.name} chose {self.active_card.name}.")

    """ is a method that walks a player through his turn by making him choose between attack and defend and calls the respective method"""

    def take_turn(self, other_player):
        card = self.active_card
        opponent = other_player.active_card
        print(f"\n{self.name}'s turn: {card.name} ({card.health} health)")
        print(f"Opponent: {opponent.name} ({opponent.health} health)")
        action = input("Defend (0) or attack (1): ").strip()
        while action not in ("0", "1"):
            action = input("Please enter 0 for defend or 1 for attack: ").strip()

        if action == "0":
            print(card.defend())
            return

        for name, details in card.attacks.items():
            print(f"{name}: {details[0]} ({details[1]} damage)")
        attack_name = input("Choose an attack by name: ").strip()
        while attack_name not in card.attacks:
            attack_name = input("Please enter an attack name from the list: ").strip()

        result = card.attack(opponent, attack_name)
        if result["hit"]:
            print(f"Hit! {result['damage']} damage.")
        else:
            print("The attack missed.")
        print(f"{opponent.name} has {opponent.health} health left.")
