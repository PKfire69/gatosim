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

# ---------------------------------------------------------------------------
# The model. A dictionary of states, each holding a dictionary of details.
# Every state has the same keys, which is what makes the functions below
# possible: they can rely on "description" and "exits" being there.
# ---------------------------------------------------------------------------
# Names: Parker Karlen, Hamid Eyyubov



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
        "transitions": ["Meepo", "FireMage"]
        "mode": True,
    },
    # Below is a card that was being worked on this is subject to some changes based on how we want to create gameplay.:w
    "Meepo": {
        "description": "Meepo is a magical cave elf that summons 5 copies of himself to fight from every front.",
        "attacks": {
            "Earth Bind": [
                "tosses a net at an enemy stopping them keeping them from play for one turn",
                100,
            ],
            "Divided We Stand": [],
        },
        "action": ["attack", "defend"],
        "health": 800,
        "transitions": ["ShadowKnight", "IceWizard"]
    },


    "FireMage": {
        "description": "A mage who attacks with fire",
        "attacks": {
            "GoldenHeart": [
                "Throws a ball of fire at the enemy",
                150
            ]
        },
        "action": ["attack", "defend"],
        "health": 700,
        "transitions": ["ShadowKnight", "StoneGolem"]
    },

    "IceWizard": {
        "description": "A wizard who uses ice to slow enemies"
        "attacks": {
    "Ice Blast": [
        "Launches an icy blast at the enemy.",
        120
    ]
},
    }
}


def spew(deck, state):
    print(deck["ShadowKnight"]["description"])
    print(deck["Meepo"]["description"])
    print(deck["Meepo"]["attacks"]["Earth Bind"])
    print(deck["Shadow Knight"]["health"])


# My teamate and I argued over if we should use a list or a dictionary item within the attacks dictionary. We came to the conclusion that we would use a list and its index to display attack information which will be used in game.

# ---------------------------------------------------------------------------
# One function that reads the model. Write yours for your project.
# ---------------------------------------------------------------------------


def describe(world, state):
    """Print one state: its description, its exits, and what is there."""
    place = world[state]
    print(state.upper())
    print(place["description"])
    print("Exits:", ", ".join(place["exits"]))
    print("Here:", ", ".join(place["items"]) if place["items"] else "nothing")


if __name__ == "__main__":
    describe(WORLD, "lobby")
