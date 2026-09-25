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
def playerturn(player1,player2, attackerhand, opponenthand):
    print(f"{player1.name}, choose a character to attack or defend with\n your options are {attackerhand['name']}")
    player1choice = input()
    while player1choice not in attackerhand:
        print("please enter a valid name from the given list")
        print(attackerhand)
        player1choice = input()
    for card in attackerhand:
        if card == 
    print("do you want to defend(0) or attack(1)")
    action1 = input()
    while action1 != "0" and action1 != "1":
        print("please enter 0 for defend or 1 for attack:")
        action1 = input()
    if action1 == "1":
        print(DECK[player1choice]["attacks"])
        print('enter the which attack you would like to execute above')
        attack(input())
        while attack not in list(DECK[player1choice]['attacks']):
            print('please type a valid attack from the list below')
            print(list(DECK[player1choice]['attacks']))
            attack = input()
        print('Choose who you want to attack from the list below')
        print(opponenthand['name'])
        oppcard = input()
        while oppcard not in opponenthand:
            print('Please enter a valid choice from the list above:')
            oppcard = input()
        variable = attack(attackerhand[player1choice],opponenthand[oppcard],attack)
        print(variable)

def is_dead(hand1,hand2):
    pass

def draw_card(name=None):
    if name is None:
        name = random.choice(list(DECK))
    card = deepcopy(DECK[name   ])
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


class card_dual:
    def __init__(self, name, description, health):
        self.name = name
        self.description = description
        self.health = health


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
        "You and your opponent will start the game by each drawing one card from a deck of 10 different characters, each with their own attacks and story"
    )
    print("You and your opponent will take turns making two options; Attack or Defend.")
    print(
        "each card has a set number of health that will you must devalue to 0.The first player to defeat 5 characters will be deemed the winner of the game"
    )
    print("Enter play to start the game")
    while input() != "play":
        print("Something went wrong: Type play")
        continue
    describe(DECK, draw_card()["name"])
    keep_playing = True
    while keep_playing:
        print("Enter player ones name:")
        player1 = player(input())
        print("Enter player twos name:")
        player2 = player(input())
        hand1 = [draw_card() for _ in range(3)]
        hand2 = [draw_card() for _ in range(3)]
        print(f"{player1} you have drawn:")
        for card in hand1:
            print(card['name'])
        print("press 1 to continue")
        while input() != "1":
            print("please try again")
            continue
        print(f"{player2} you have drawn: {hand2}")
        while player1.score < 5 and player2.score < 5:
            playerturn(player1,player2,hand1,hand2)


# My teamate and I argued over if we should use a list or a dictionary item within the attacks dictionary. We came to the conclusion that we would use a list and its index to display attack information which will be used in game.

# ---------------------------------------------------------------------------
# One function that reads the model. Write yours for your project.
# ---------------------------------------------------------------------------


def describe(world, state):
    """Print one state: its description, its exits, and what is there."""
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
