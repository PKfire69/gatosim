"""CSci 1923, Session 4 studio.

Build the world model for one pod member's project.

This file shows the shape using two rooms from The Vault. Nobody is building
an escape room, so none of this is your answer. It is the shape, not the
content. Replace it with the states, items, and transitions from the chosen
project, whatever your track calls those things.

ONE TASK, TWENTY-FIVE MINUTES:
  Build at least five states for the chosen project, each with a description,
  at least one list, and its transitions to other states. Then write ONE
  function that reads the model. describe() below is an example of one.

  If you finish, add nested containers (a list of dictionaries inside a
  state), then write a second function. Nobody is expected to get there.

ROLES TODAY:
  The person whose project this is does not touch the keyboard. They answer
  questions and nothing else. Of the other two, the less confident one
  drives. The third navigates and will be today's scribe.
"""

import random
from copy import deepcopy

# ---------------------------------------------------------------------------
# The model. A dictionary of states, each holding a dictionary of details.
# Every state has the same keys, which is what makes the functions below
# possible: they can rely on "description" and "exits" being there.
# ---------------------------------------------------------------------------
# Names: Parker Karlen, Hamid Eyyubov


BASE_HIT_CHANCE = 0.80

DECK = {
    "ShadowKnight": {
        "description": "A phantom clad in obsidian armor, he strikes from the city's dark alleys before his targets even know he exists. Corrupt warlords whisper his name in fear, knowing no shield can block a blade born of shadow.",
        "attacks": {
            "Dark Blade Slash": [
                "Coated in dense dark energy, Shadow Knight's blade cuts through the air to leave a trail of razor-sharp shadow that shatters enemy defenses on impact.",
                200,
            ],
        },
        "action": ["attack", "defend"],
        "health": 1000,
        "defend": {
            "description": "Merges with the shadows to evade the next attack.",
            "hit_chance_reduction": 0.30,
        },
        "mode": True,
    },
    # Below is a card that was being worked on this is subject to some changes based on how we want to create gameplay.
    "Meepo": {
        "description": "Meepo is a magical cave elf that summons 5 copies of himself to fight from every front.",
        "attacks": {
            "Earth Bind": [
                "tosses a net at an enemy stopping them keeping them from play for one turn",
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
        "description": "A mage who attacks with fire",
        "attacks": {"GoldenHeart": ["Throws a ball of fire at the enemy", 150]},
        "action": ["attack", "defend"],
        "health": 700,
        "defend": {
            "description": "Raises a wall of flame to obscure the next attack.",
            "hit_chance_reduction": 0.25,
        },
    },
    "IceWizard": {
        "description": "A wizard who uses ice to slow enemies",
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
            "Boulder Slam": ["Smashes the enemy with a massive stone fist.", 180],
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
            "Lightning Fist": ["Strikes the enemy with an electrified punch.", 170],
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


def draw_card(name=None):
    if name is None:
        name = random.choice(list(DECK))
    card = deepcopy(DECK[name])
    card["name"] = name
    card["defending"] = False
    return card


def defend(card):
    if card["health"] <= 0:
        raise ValueError("A defeated character cannot defend.")
    card["defending"] = True
    return card["defend"]["description"]


def attack(attacker, opponent, attack_name):
    if attacker["health"] <= 0 or opponent["health"] <= 0:
        raise ValueError("Both characters must be alive to attack.")
    attack_damage = attacker["attacks"][attack_name][1]
    hit_chance = BASE_HIT_CHANCE
    if opponent.get("defending", False):
        hit_chance -= opponent["defend"]["hit_chance_reduction"]
    hit_chance = max(0.0, min(1.0, hit_chance))
    hit = random.random() < hit_chance
    opponent["defending"] = False
    damage = min(attack_damage, opponent["health"]) if hit else 0
    opponent["health"] -= damage
    return {"hit": hit, "hit_chance": hit_chance, "damage": damage}


def promptcontinue(zero):
    while input() != "1":
        print("please try again")
        continue


class player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []
        self.active_card = None


class card_dual:
    def __init__(self, name, description, health):
        self.name = name
        self.description = description
        self.health = health


def choose_card(game_player):
    print(f"{game_player.name}, choose your active character:")
    for i in range(3):
        card = game_player.hand[i]
        print(f"{i + 1}. {card['name']} — {card['health']} health")

    choice = input("Enter 1, 2, or 3: ").strip()
    while choice not in ("1", "2", "3"):
        choice = input("Please enter 1, 2, or 3: ").strip()

    game_player.active_card = game_player.hand[int(choice) - 1]


def take_turn(current_player, other_player):
    card = current_player.active_card
    opponent = other_player.active_card
    print(f"{current_player.name}'s turn: {card['name']} ({card['health']} health)")
    print(f"Opponent: {opponent['name']} ({opponent['health']} health)")
    action = input("Defend (0) or attack (1): ").strip()
    while action not in ("0", "1"):
        action = input("Please enter 0 for defend or 1 for attack: ").strip()

    if action == "0":
        print(defend(card))
    else:
        for name, details in card["attacks"].items():
            print(f"{name}: {details[0]} ({details[1]} damage)")
        attack_name = input("Choose an attack by name: ").strip()
        while attack_name not in card["attacks"]:
            attack_name = input("Please enter an attack name from the list: ").strip()

        result = attack(card, opponent, attack_name)
        if result["hit"]:
            print(f"Hit! {result['damage']} damage.")
        else:
            print("The attack missed.")
        print(f"{opponent['name']} has {opponent['health']} health left.")


def main():
    print(
        "Hello, this is not only a card game but a game of chance. You will be pitted against your friend where the choices you make will effect the outcome of the game"
    )
    print("Press y to continue:")
    while input() != "y":
        continue
    print(
        "----------------------------------------------------------------------------"
    )
    print(
        "Each player draws three cards from a deck of 10 characters and chooses one active character for the battle."
    )
    print("You and your opponent will take turns making two options; Attack or Defend.")
    print(
        "Take turns until one active character reaches 0 health. The other player wins the battle."
    )
    print("Enter play to start the game")
    while input() != "play":
        print("Something went wrong: Type play")
        continue
    player1 = player(input("Enter player one's name: "))
    player2 = player(input("Enter player two's name: "))
    for i in range(3):
        player1.hand.append(draw_card())
        player2.hand.append(draw_card())

    choose_card(player1)
    choose_card(player2)
    current_player = player1
    other_player = player2

    while player1.active_card["health"] > 0 and player2.active_card["health"] > 0:
        take_turn(current_player, other_player)
        if other_player.active_card["health"] == 0:
            print(f"{current_player.name} wins the battle!")
            break

        if current_player == player1:
            current_player = player2
            other_player = player1
        else:
            current_player = player1
            other_player = player2


def spew(deck, state):
    describe(deck, state)


# My teamate and I argued over if we should use a list or a dictionary item within the attacks dictionary. We came to the conclusion that we would use a list and its index to display attack information which will be used in game.

# ---------------------------------------------------------------------------
# One function that reads the model. Write yours for your project.
# ---------------------------------------------------------------------------


def describe(world, state):
    card = world[state]
    print(state.upper())
    print(card["description"])
    print("Health:", card["health"])
    print("Actions:", ", ".join(card["action"]))
    for name, details in card["attacks"].items():
        print(f"{name}: {details[0]} ({details[1]} damage)")
    defended_chance = max(0.0, BASE_HIT_CHANCE - card["defend"]["hit_chance_reduction"])
    print("Defend:", card["defend"]["description"])
    print(f"Opponent's next hit chance: {BASE_HIT_CHANCE:.0%} -> {defended_chance:.0%}")


if __name__ == "__main__":
    main()
