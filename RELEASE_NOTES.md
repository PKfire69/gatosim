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

## What I had to change, and why

The game now keeps its data and state in objects. `Deck` owns a list of ten
`Card` objects instead of relying on the global `DECK` dictionary. Drawing a card
copies one of these objects, so two players can draw the same character without
sharing health, attacks, or defense state.

`Card` handles its own attacks, defense, and description. `Player` stores a hand
and selects an active card from it. `Game` owns the deck, players, and turn order,
and its `run()` method handles the battle. These changes put each operation next
to the data it uses and remove the need to pass game state between separate
functions. The game still starts from `world_model_starter.py`.

`AttackAction` and `DefendAction` inherit from `TurnAction`. Both override
`perform()` and call the parent method to check that both cards are alive before
performing their own action. This gives the two actions a shared check while
keeping their different behavior clear.

Two special methods make the objects easier to use: `Card.__str__()` provides a
readable card summary, and `Deck.__len__()` lets the game use `len(deck)` to count
its cards. The existing damage, hit chances, card choices, and one-battle rules
stay the same.

## Looking ahead

A planned `Game.play_tournament()` method would use recursion to resolve the two halves of a tournament bracket; it is not implemented yet.
The `Deck.find_card()` method checks cards one at a time, so its efficiency will matter as the number of cards grows.
The `Game.take_turn()` method displays the available attacks each turn, so its efficiency will matter as cards gain more attacks.
