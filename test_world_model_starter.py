import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import world_model_starter as game


class CombatTests(unittest.TestCase):
    def setUp(self):
        self.deck = game.Deck()

    def test_all_ten_characters_can_attack_and_defend(self):
        self.assertEqual(len(self.deck), 10)
        for template in self.deck.cards:
            for attack_name in template.attacks:
                with self.subTest(character=template.name, attack=attack_name):
                    attacker = self.deck.draw_card(template.name)
                    opponent = self.deck.draw_card("StoneGolem")
                    self.assertGreater(attacker.health, 0)
                    self.assertTrue(attacker.defend())
                    with patch("world_model_starter.random.random", return_value=0.0):
                        result = opponent.attack(attacker, "Boulder Slam")
                    self.assertLess(result["hit_chance"], 0.80)
                    self.assertGreater(result["hit_chance"], 0.0)
                    with patch("world_model_starter.random.random", return_value=0.0):
                        result = attacker.attack(opponent, attack_name)
                    self.assertTrue(result["hit"])
                    self.assertGreater(result["damage"], 0)

    def test_defending_turns_a_hit_into_a_miss(self):
        attacker = self.deck.draw_card("FireMage")
        unguarded = self.deck.draw_card("ShadowKnight")
        guarded = self.deck.draw_card("ShadowKnight")
        guarded.defend()
        with patch("world_model_starter.random.random", return_value=0.60):
            ordinary = attacker.attack(unguarded, "GoldenHeart")
            defended = attacker.attack(guarded, "GoldenHeart")
        self.assertTrue(ordinary["hit"])
        self.assertEqual(unguarded.health, 850)
        self.assertFalse(defended["hit"])
        self.assertEqual(defended["damage"], 0)
        self.assertEqual(guarded.health, 1000)
        self.assertAlmostEqual(defended["hit_chance"], 0.50)

    def test_defense_expires_after_either_a_hit_or_a_miss(self):
        for first_roll in (0.10, 0.60):
            with self.subTest(first_roll=first_roll):
                attacker = self.deck.draw_card("FireMage")
                opponent = self.deck.draw_card("ShadowKnight")
                opponent.defend()
                with patch(
                    "world_model_starter.random.random", side_effect=[first_roll, 0.60]
                ):
                    first = attacker.attack(opponent, "GoldenHeart")
                    second = attacker.attack(opponent, "GoldenHeart")
                self.assertEqual(first["hit"], first_roll < 0.50)
                self.assertTrue(second["hit"])
                self.assertAlmostEqual(second["hit_chance"], 0.80)

    def test_repeated_defense_does_not_stack(self):
        attacker = self.deck.draw_card("FireMage")
        opponent = self.deck.draw_card("ShadowKnight")
        opponent.defend()
        opponent.defend()
        with patch("world_model_starter.random.random", return_value=0.40):
            result = attacker.attack(opponent, "GoldenHeart")
        self.assertTrue(result["hit"])
        self.assertAlmostEqual(result["hit_chance"], 0.50)

    def test_combat_does_not_change_other_draws_or_deck(self):
        attacker = self.deck.draw_card("FireMage")
        opponent = self.deck.draw_card("ShadowKnight")
        another_draw = self.deck.draw_card("ShadowKnight")
        opponent.defend()
        with patch("world_model_starter.random.random", return_value=0.0):
            attacker.attack(opponent, "GoldenHeart")
        self.assertEqual(opponent.health, 850)
        self.assertEqual(another_draw.health, 1000)
        self.assertFalse(another_draw.defending)
        self.assertEqual(self.deck.find_card("ShadowKnight").health, 1000)
        self.assertFalse(self.deck.find_card("ShadowKnight").defending)

    def test_attack_lists_are_independent_between_draws_and_deck(self):
        first = self.deck.draw_card("FireMage")
        second = self.deck.draw_card("FireMage")

        first.attacks["GoldenHeart"][1] = 1

        self.assertEqual(second.attacks["GoldenHeart"][1], 150)
        self.assertEqual(self.deck.find_card("FireMage").attacks["GoldenHeart"][1], 150)

    def test_health_stops_at_zero_and_defeated_characters_cannot_act(self):
        attacker = self.deck.draw_card("FireMage")
        opponent = self.deck.draw_card("ShadowKnight")
        opponent.health = 10
        with patch("world_model_starter.random.random", return_value=0.0):
            result = attacker.attack(opponent, "GoldenHeart")
        self.assertEqual(result["damage"], 10)
        self.assertEqual(opponent.health, 0)
        with self.assertRaises(ValueError):
            opponent.defend()
        with self.assertRaises(ValueError):
            opponent.attack(attacker, "Dark Blade Slash")
        with self.assertRaises(ValueError):
            attacker.attack(opponent, "GoldenHeart")


class TurnTests(unittest.TestCase):
    def setUp(self):
        self.battle = game.Game()

    def test_card_selection_keeps_the_selected_copy_and_its_health(self):
        current = game.Player("Ada")
        other = game.Player("Bob")
        current.hand.append(self.battle.deck.draw_card("FireMage"))
        current.hand.append(self.battle.deck.draw_card("FireMage"))
        current.hand.append(self.battle.deck.draw_card("ShadowKnight"))
        current.hand[1].health = 300

        with patch("builtins.input", side_effect=["wrong", "0", "4", "2"]):
            with redirect_stdout(io.StringIO()):
                current.choose_card()

        self.assertIs(current.active_card, current.hand[1])
        self.assertEqual(current.active_card.health, 300)
        self.assertEqual(current.hand[0].health, 700)
        self.assertEqual(other.hand, [])

    def test_turn_retries_invalid_input_and_applies_defense_and_damage(self):
        current = game.Player("Ada")
        other = game.Player("Bob")
        current.active_card = self.battle.deck.draw_card("FireMage")
        other.active_card = self.battle.deck.draw_card("ShadowKnight")
        output = io.StringIO()
        self.battle.current_player = other
        self.battle.other_player = current

        with patch("builtins.input", side_effect=["wrong", "0"]):
            with redirect_stdout(output):
                self.battle.take_turn()
        self.assertTrue(other.active_card.defending)
        self.battle.current_player = current
        self.battle.other_player = other

        with patch(
            "builtins.input", side_effect=["wrong", "1", "wrong", "GoldenHeart"]
        ):
            with patch("world_model_starter.random.random", return_value=0.60):
                with redirect_stdout(output):
                    self.battle.take_turn()
        self.assertEqual(other.active_card.health, 1000)
        self.assertFalse(other.active_card.defending)
        self.assertIn("miss", output.getvalue().lower())

        with patch("builtins.input", side_effect=["1", "GoldenHeart"]):
            with patch("world_model_starter.random.random", return_value=0.60):
                with redirect_stdout(output):
                    self.battle.take_turn()
        self.assertEqual(other.active_card.health, 850)
        self.assertEqual(current.active_card.health, 700)
        self.assertIn("150", output.getvalue())
        self.assertIn("850", output.getvalue())
        self.assertIn("Ada's turn: FireMage (700 health)", output.getvalue())

    def test_run_alternates_after_a_miss_and_stops_at_knockout(self):
        cards = [
            self.battle.deck.draw_card("FireMage"),
            self.battle.deck.draw_card("ShadowKnight"),
            self.battle.deck.draw_card("FireMage"),
            self.battle.deck.draw_card("ShadowKnight"),
            self.battle.deck.draw_card("FireMage"),
            self.battle.deck.draw_card("ShadowKnight"),
        ]
        cards[2].health = 250
        cards[5].health = 200
        answers = [
            "y",
            "play",
            "Ada",
            "Bob",
            "2",
            "3",
            "1",
            "GoldenHeart",
            "1",
            "Dark Blade Slash",
            "1",
            "GoldenHeart",
            "1",
            "Dark Blade Slash",
        ]
        output = io.StringIO()

        with patch("builtins.input", side_effect=answers):
            with patch("world_model_starter.Deck.draw_card", side_effect=cards):
                with patch(
                    "world_model_starter.random.random", side_effect=[0.99, 0, 0, 0]
                ):
                    with redirect_stdout(output):
                        self.battle.run()

        self.assertEqual(cards[2].health, 0)
        self.assertEqual(cards[5].health, 50)
        self.assertEqual(cards[0].health, 700)
        self.assertEqual(cards[1].health, 1000)
        self.assertEqual(cards[3].health, 1000)
        self.assertEqual(cards[4].health, 700)
        self.assertIs(self.battle.player1.active_card, cards[2])
        self.assertIs(self.battle.player2.active_card, cards[5])
        self.assertIn("Bob", output.getvalue().splitlines()[-1])


class ObjectStateTests(unittest.TestCase):
    def test_constructors_do_not_start_interactive_play(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=AssertionError("Unexpected input")):
            with redirect_stdout(output):
                battle = game.Game()
                player = game.Player("Ada")
                card = battle.deck.draw_card("FireMage")
                opponent = battle.deck.draw_card("ShadowKnight")
                game.AttackAction(card, opponent)
                game.DefendAction(card, opponent)

        self.assertEqual(output.getvalue(), "")
        self.assertIsNone(battle.player1)
        self.assertIsNone(battle.player2)
        self.assertIsNone(battle.current_player)
        self.assertIsNone(battle.other_player)
        self.assertEqual(player.hand, [])
        self.assertIsNone(player.active_card)
        self.assertEqual(player.score, 0)

    def test_card_copies_the_supplied_nested_data(self):
        data = {
            "description": "A mage who attacks with fire",
            "attacks": {"GoldenHeart": ["Throws a ball of fire at the enemy", 150]},
            "action": ["attack", "defend"],
            "health": 700,
            "defend": {
                "description": "Raises a wall of flame to obscure the next attack.",
                "hit_chance_reduction": 0.25,
            },
        }
        card = game.Card("FireMage", data)
        card.attacks["GoldenHeart"][1] = 1
        card.actions.append("rest")
        card.health = 20

        self.assertEqual(data["attacks"]["GoldenHeart"][1], 150)
        self.assertEqual(data["action"], ["attack", "defend"])
        self.assertEqual(data["health"], 700)

    def test_game_decks_have_independent_nested_state(self):
        first = game.Game()
        second = game.Game()
        first_card = first.deck.find_card("FireMage")
        first_card.health = 1
        first_card.attacks["GoldenHeart"][1] = 1
        first_card.actions.append("rest")
        first_card.defend()

        first_draw = first.deck.draw_card("FireMage")
        self.assertEqual(first_draw.health, 1)
        self.assertEqual(first_draw.attacks["GoldenHeart"][1], 1)
        self.assertTrue(first_draw.defending)
        second_card = second.deck.draw_card("FireMage")
        self.assertEqual(second_card.health, 700)
        self.assertEqual(second_card.attacks["GoldenHeart"][1], 150)
        self.assertEqual(second_card.actions, ["attack", "defend"])
        self.assertFalse(second_card.defending)

    def test_random_draw_copies_the_selected_deck_card(self):
        deck = game.Deck()
        template = deck.find_card("Meepo")
        with patch("world_model_starter.random.choice", return_value=template):
            drawn = deck.draw_card()

        self.assertEqual(drawn.name, "Meepo")
        self.assertEqual(drawn.attacks["Divided We Stand"][1], 160)
        drawn.attacks["Divided We Stand"][1] = 1
        drawn.actions.append("rest")
        drawn.defend()
        self.assertEqual(template.attacks["Divided We Stand"][1], 160)
        self.assertEqual(template.actions, ["attack", "defend"])
        self.assertFalse(template.defending)

    def test_unknown_card_name_is_rejected(self):
        deck = game.Deck()
        with self.assertRaises(KeyError):
            deck.find_card("Unknown")
        with self.assertRaises(KeyError):
            deck.draw_card("Unknown")

    def test_card_preview_and_summary_show_current_state(self):
        card = game.Deck().draw_card("FireMage")
        card.health = 300
        output = io.StringIO()
        with redirect_stdout(output):
            card.describe()

        self.assertEqual(str(card), "FireMage (300 health)")
        self.assertEqual(
            output.getvalue(),
            "FIREMAGE\n"
            "A mage who attacks with fire\n"
            "Health: 300\n"
            "Actions: attack, defend\n"
            "GoldenHeart: Throws a ball of fire at the enemy (150 damage)\n"
            "Defend: Raises a wall of flame to obscure the next attack.\n"
            "Opponent's next hit chance: 80% -> 55%\n",
        )


class ActionTests(unittest.TestCase):
    def test_attack_action_retries_names_and_applies_damage(self):
        deck = game.Deck()
        card = deck.draw_card("FireMage")
        opponent = deck.draw_card("ShadowKnight")
        output = io.StringIO()
        with patch("builtins.input", side_effect=["goldenheart", "GoldenHeart"]):
            with patch("world_model_starter.random.random", return_value=0.0):
                with redirect_stdout(output):
                    game.AttackAction(card, opponent).perform()

        self.assertEqual(opponent.health, 850)
        self.assertEqual(card.health, 700)
        self.assertFalse(card.defending)
        self.assertIn("Hit! 150 damage.", output.getvalue())
        self.assertIn("ShadowKnight has 850 health left.", output.getvalue())

    def test_defend_action_protects_the_card_without_damaging_opponent(self):
        deck = game.Deck()
        card = deck.draw_card("FireMage")
        opponent = deck.draw_card("ShadowKnight")
        output = io.StringIO()
        with patch("builtins.input", side_effect=AssertionError("Unexpected input")):
            with redirect_stdout(output):
                game.DefendAction(card, opponent).perform()

        self.assertTrue(card.defending)
        self.assertEqual(card.health, 700)
        self.assertEqual(opponent.health, 1000)
        self.assertFalse(opponent.defending)
        self.assertIn("Raises a wall of flame", output.getvalue())

    def test_actions_reject_a_defeated_participant_before_prompting(self):
        deck = game.Deck()
        for action_class in (game.TurnAction, game.AttackAction, game.DefendAction):
            for defeated_side in ("card", "opponent"):
                with self.subTest(action=action_class.__name__, side=defeated_side):
                    card = deck.draw_card("FireMage")
                    opponent = deck.draw_card("ShadowKnight")
                    if defeated_side == "card":
                        card.health = 0
                    else:
                        opponent.health = 0
                    output = io.StringIO()
                    with patch(
                        "builtins.input", side_effect=AssertionError("Unexpected input")
                    ):
                        with redirect_stdout(output):
                            with self.assertRaises(ValueError):
                                action_class(card, opponent).perform()

                    self.assertFalse(card.defending)
                    self.assertFalse(opponent.defending)
                    self.assertEqual(output.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
