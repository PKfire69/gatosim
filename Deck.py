import random
from Cards import Card, Mage, Guardian

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

    """This is the function that draws a card from the deck which is instaniated at initialization.
        It was changed to a recursive function where the random module is still used and to pick a
        side of the deck which then continues slicing the deck until there is only one element and
        recursively returns the chosen card and removes the chosen card from the available cards"""

    def random_choice(self, first_half, second_half):
        return random.choice([first_half, second_half])

    def draw_card(self, deck=False):
        if not deck:
            copy_deck = self.available
        else:
            copy_deck = deck
        i = len(copy_deck) // 2
        left_half = copy_deck[:i]
        right_half = copy_deck[i:]
        if len(copy_deck) == 1:
            name = copy_deck[0]
            card_class = self.CARD_CLASSES[name]
            self.available.remove(name)

            return card_class(name, self.cards[name])
        else:
            return self.draw_card(self.random_choice(left_half, right_half))

