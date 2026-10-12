import random

# Names: Parker Karlen, Hamid Eyyubov, Cole Stojevich

# My teamate and I argued over if we should use a list or a dictionary item within the attacks dictionary. We came to the conclusion that we would use a list and its index to display attack information which will be used in game.


class Card:
    """this class keeps tracks of cards and its attributes"""

    BASE_HIT_CHANCE = 0.80

    """Instantiates the card attributes"""

    def __init__(self, name, card_data):
        self.name = name
        self.description = card_data["description"]
        self.attacks = card_data["attacks"]
        self.actions = card_data["action"]
        self.health = card_data["health"]
        self.max_health = card_data["health"]
        self.defending = False
        self.defense_desc = card_data["defend"]["description"]
        self.hit_reduction = card_data["defend"]["hit_chance_reduction"]

    """ returns a string to be printed to define the health of a character"""

    def __str__(self):
        return f"{self.name} - {self.health} health"

    def __lt__(self, other):
        return self.health < other.health

    def is_alive(self):
        return self.health > 0

    def defend(self):
        self.defending = True
        return self.defense_desc

    def hit_chance_against(self, target):
        chance = self.BASE_HIT_CHANCE
        if target.defending:
            chance -= target.hit_reduction
        return max(0.0, chance)

    def attack(self, target, attack_name):
        """is a function that defines the cards attacking eachother by using the card instantiaions and is_alive() method"""
        if not self.is_alive() or not target.is_alive():
            raise ValueError("Both characters must be alive to attack.")
        attack_damage = self.attacks[attack_name][1]
        hit_chance = self.hit_chance_against(target)
        hit = random.random() < hit_chance
        target.defending = False
        damage = min(attack_damage, target.health) if hit else 0
        target.health -= damage
        return {"hit": hit, "hit_chance": hit_chance, "damage": damage}

    def describe(self):
        print(self.name.upper())
        print(self.description)
        print("Health:", self.health)
        print("Actions:", ", ".join(self.actions))
        for name, details in self.attacks.items():
            print(f"{name}: {details[0]} ({details[1]} damage)")
        defended_chance = max(0.0, self.BASE_HIT_CHANCE - self.hit_reduction)
        print("Defend:", self.defense_desc)
        print(
            f"Opponent's next hit chance: {self.BASE_HIT_CHANCE:.0%} -> {defended_chance:.0%}"
        )


class Mage(Card):
    """cut through half of the target's defense."""

    def hit_chance_against(self, target):
        """Return the hit chance with the target's defense halved."""
        chance = self.BASE_HIT_CHANCE
        if target.defending:
            chance -= target.hit_reduction / 2
        return max(0.0, chance)


class Guardian(Card):
    """recovers some health when it defends."""

    HEAL_AMOUNT = 50

    def defend(self):
        """attack and recover a little health."""
        description = super().defend()
        self.health = min(self.max_health, self.health + self.HEAL_AMOUNT)
        return f"{description} Recovers {self.HEAL_AMOUNT} health."


class Deck:
    """is a new addition in v.05 by creating character classes that have different attributes"""

    CARD_CLASSES = {
        "ShadowKnight": Card,
        "Meepo": Card,
        "FireMage": Mage,
        "IceWizard": Mage,
        "StoneGolem": Guardian,
        "WindArcher": Card,
        "ThunderMonk": Mage,
        "ForestGuardian": Guardian,
        "SunPaladin": Guardian,
        "SeaSerpent": Card,
    }

    """Instantiates the main deck of the game which is used by its draw_card method to instantiated cards into the card class"""

    def __init__(self):
        self.cards = {
            "ShadowKnight": {
                "description": "A phantom clad in obsidian armor, he strikes from the city's shadows.",
                "attacks": {
                    "Dark Blade Slash": [
                        "Coated in dense dark energy, Shadow Knight's blade cuts through the air to leave a trail of razor-sharp shadow that shatters enemy defenses on impact.",
                        200,
                    ]
                },
                "action": ["attack", "defend"],
                "health": 1000,
                "defend": {
                    "description": "Merges with the shadows to evade the next attack.",
                    "hit_chance_reduction": 0.30,
                },
            },
            "Meepo": {
                "description": "Meepo is a magical cave elf that summons 5 copies of himself to fight from every front.",
                "attacks": {
                    "Earth Bind": [
                        "Tosses a net at an enemy, keeping them from play for one turn.",
                        100,
                    ],
                    "Divided We Stand": [
                        "Summons five copies to strike the enemy together.",
                        160,
                    ],
                },
                "action": ["attack", "defend"],
                "health": 800,
                "defend": {
                    "description": "Creates decoys to confuse the next attacker.",
                    "hit_chance_reduction": 0.35,
                },
            },
            "FireMage": {
                "description": "A mage who attacks with fire.",
                "attacks": {
                    "GoldenHeart": ["Throws a ball of fire at the enemy.", 150]
                },
                "action": ["attack", "defend"],
                "health": 700,
                "defend": {
                    "description": "Raises a wall of flame to obscure the next attack.",
                    "hit_chance_reduction": 0.25,
                },
            },
            "IceWizard": {
                "description": "A wizard who uses ice to slow enemies.",
                "attacks": {"Ice Blast": ["Launches an icy blast at the enemy.", 120]},
                "action": ["attack", "defend"],
                "health": 750,
                "defend": {
                    "description": "Summons a snowstorm to hide from the next attack.",
                    "hit_chance_reduction": 0.30,
                },
            },
            "StoneGolem": {
                "description": "An ancient guardian carved from mountain stone.",
                "attacks": {
                    "Boulder Slam": [
                        "Smashes the enemy with a massive stone fist.",
                        180,
                    ],
                },
                "action": ["attack", "defend"],
                "health": 1200,
                "defend": {
                    "description": "Raises a stone barrier to intercept the next attack.",
                    "hit_chance_reduction": 0.40,
                },
            },
            "WindArcher": {
                "description": "A swift archer whose arrows ride the wind.",
                "attacks": {
                    "Gale Arrow": ["Fires an arrow carried by a powerful gust.", 140],
                },
                "action": ["attack", "defend"],
                "health": 650,
                "defend": {
                    "description": "Dashes aside on a gust of wind to dodge the next attack.",
                    "hit_chance_reduction": 0.45,
                },
            },
            "ThunderMonk": {
                "description": "A mountain monk who channels lightning through his fists.",
                "attacks": {
                    "Lightning Fist": [
                        "Strikes the enemy with an electrified punch.",
                        170,
                    ],
                },
                "action": ["attack", "defend"],
                "health": 850,
                "defend": {
                    "description": "Moves with lightning speed to evade the next attack.",
                    "hit_chance_reduction": 0.30,
                },
            },
            "ForestGuardian": {
                "description": "A living tree that protects the creatures of the forest.",
                "attacks": {
                    "Vine Lash": ["Whips the enemy with a thorn-covered vine.", 130],
                },
                "action": ["attack", "defend"],
                "health": 1100,
                "defend": {
                    "description": "Weaves a screen of branches to block the next attack.",
                    "hit_chance_reduction": 0.35,
                },
            },
            "SunPaladin": {
                "description": "A knight who carries a shield bright as the morning sun.",
                "attacks": {
                    "Radiant Strike": ["Swings a sword glowing with sunlight.", 160],
                },
                "action": ["attack", "defend"],
                "health": 1000,
                "defend": {
                    "description": "Flashes a radiant shield to disrupt the next attack.",
                    "hit_chance_reduction": 0.40,
                },
            },
            "SeaSerpent": {
                "description": "A creature of the deep that commands waves and sea mist.",
                "attacks": {
                    "Tidal Crash": ["Sends a crushing wave into the enemy.", 190],
                },
                "action": ["attack", "defend"],
                "health": 900,
                "defend": {
                    "description": "Disappears into sea mist to evade the next attack.",
                    "hit_chance_reduction": 0.25,
                },
            },
        }
        self.available = list(self.cards)

    def __len__(self):
        return len(self.available)

    """This is the function that draws a card from the deck which is instaniated at initialization"""

    def draw_card(self):
        name = random.choice(self.available)
        self.available.remove(name)
        card_class = self.CARD_CLASSES[name]
        return card_class(name, self.cards[name])


class Player:
    """instantiates players with different attributes stated below"""

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        self.active_card = None

    """Is the string dunder method that that returns a string of the players name and their respected score """

    def __str__(self):
        return f"{self.name} (score: {self.score})"

    """is called at the beginning of the game to draw 3 cards into a players hand and sorts them alphabetically"""

    def draw_hand(self, deck, size=3):
        while len(self.hand) < size:
            self.hand.append(deck.draw_card())
        self.hand.sort()

    """is a method that is called to make a player choose an active card for battle"""

    def choose_card(self):
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

    """ This is the main loop of the game and keeps the game running until one of the active cards is dead"""

    def play(self):
        self.setup()
        current, other = self.players
        while current.active_card.is_alive() and other.active_card.is_alive():
            current.take_turn(other)
            if not other.active_card.is_alive():
                current.score += 1
                print(f"\n{current.name} wins the battle!")
                break
            current, other = other, current


if __name__ == "__main__":
    Game().play()
