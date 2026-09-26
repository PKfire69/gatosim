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

