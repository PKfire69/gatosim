# Release Notes — Studio Card 7

## Class update

Run the game with `python world_model_starter.py`.

Each card drawn from `DECK` is now a `Card` object with its own health, attacks,
and defense state. The old `defend(card)` function moved inside the class as
`card.defend()`. Attack and turn handling use attributes such as `card.health`.
The battle rules are unchanged.

# Release Notes — v0.1

## What works



1) Two players input their names and play turn based battle
2) Deck contains 10 characters saved in a nested dictionary
3) Each character has description, defense, attacks(not a single attack type), health
4) Each user receives 3 cards(randomly) and chooses one active character
5) They can either attack or defend
6) Attacks can hit or miss. It has a base 80 percent chance of hitting.
7) Health cannot fall below zero
8) Battle ends when active character is dead
9) If input is incorrect it asks for the input again


## What does not work yet
1) Other characters can't repleace each other after they got defeated
2) The opening "y" prompt repeats silently after invalid input

## What I would change
I wanna change how attack details are stored.Right now, every attack uses list which holds its description and damage.
code must remember that index 0 means description and that 1 means damage. it makes the code harder to read and easier
to missuse .

# Release Notes - v0.5:

## What was changed:

- Moved global variable dictionary into a class its own class that is assigned to instance variable called cards on initilization.
- Created a class called

# Release Notes

## v0.5

### What I had to change, and why

**The nested dictionary became objects.** In v0.1 every card was a dictionary and the functions reached into it with keys like `card["health"]`. The card data still lives in a dictionary inside `Deck`, but `Deck.draw_card` now builds a `Card` instance from it, so health, the defending flag and the attacks belong to the card itself.

**The global state went away.** `BASE_HIT_CHANCE` is now a class attribute on `Card`, and `Game` owns the deck and the two players. `Game.play()` runs the whole battle, so `main.py` only has to call `Game().play()`. Before, the loop and the setup were loose code at the bottom of the file that passed `current_player` and `other_player` into every function.

**Attack and defend moved onto `Card`.** `Game.attack(attacker, opponent, ...)` took two cards and changed one of them. It is now `card.attack(target, attack_name)`, and defending is `card.defend()`. The old `Card.defend` attribute collided with the idea of a defend action, so the flag is now `defending`. `Game` kept the rules text and the turn loop.

**Inheritance.** `Card` is the base class. `Mage` overrides `hit_chance_against` so its spells only lose half the target's defend bonus. `Guardian` overrides `defend` and calls `super().defend()` before healing 50 health, capped at `max_health`. `Deck.CARD_CLASSES` maps each of the ten characters to its class, so v0.1's roster numbers are unchanged.

**Dunder methods.** `Card.__str__` prints a card as "name - health" in the hand menu. `Card.__lt__` lets `Player.draw_hand` sort a hand with `self.hand.sort()`. `Deck.__len__` lets `draw_card` check `len(self) == 0`, and the empty-deck check reads the same way.

