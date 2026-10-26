import random

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
    def to_dict(self):
        return {
            "type": type(self).__name__,
            "cardName": self.name,
            "charDescription": self.description,
            "attacks": self.attacks,
            "actions": self.actions,
            "health": self.health,
            "maxHealth": self.max_health,
            "defending": self.defending,
            "defense_desc": self.defense_desc,
            "hit_reduction": self.hit_reduction,
        }

    def from_dict(data):
        card_data = {
            "description": data["charDescription"],
            "attacks": data["attacks"],
            "action": data["actions"],
            "health": data["maxHealth"],
            "defend": {
                "description": data["defense_desc"],
                "hit_chance_reduction": data["hit_reduction"],
            },
        }
        if data["type"] == "Mage":
            card = Mage(data["cardName"], card_data)
        elif data["type"] == "Guardian":
            card = Guardian(data["cardName"], card_data)
        else:
            card = Card(data["cardName"], card_data)
        card.health = data["health"]
        card.defending = data["defending"]
        return card


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
