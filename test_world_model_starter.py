import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import world_model_starter as game
from world_model_starter import DECK, attack, defend, draw_card


class CombatTests(unittest.TestCase):
    def test_all_ten_characters_can_attack_and_defend(self):
        self.assertEqual(len(DECK), 10)
        for name, template in DECK.items():
            for attack_name in template["attacks"]:
                with self.subTest(character=name, attack=attack_name):
                    attacker = draw_card(name)
                    opponent = draw_card("StoneGolem")
                    self.assertGreater(attacker["health"], 0)
                    self.assertTrue(defend(attacker))
                    with patch("world_model_starter.random.random", return_value=0.0):
                        result = attack(opponent, attacker, "Boulder Slam")
                    self.assertLess(result["hit_chance"], 0.80)
                    self.assertGreater(result["hit_chance"], 0.0)
                    with patch("world_model_starter.random.random", return_value=0.0):
                        result = attack(attacker, opponent, attack_name)
                    self.assertTrue(result["hit"])
                    self.assertGreater(result["damage"], 0)

    def test_defending_turns_a_hit_into_a_miss(self):
        attacker = draw_card("FireMage")
        unguarded = draw_card("ShadowKnight")
        guarded = draw_card("ShadowKnight")
        defend(guarded)
        with patch("world_model_starter.random.random", return_value=0.60):
            ordinary = attack(attacker, unguarded, "GoldenHeart")
            defended = attack(attacker, guarded, "GoldenHeart")
        self.assertTrue(ordinary["hit"])
        self.assertEqual(unguarded["health"], 850)
        self.assertFalse(defended["hit"])
        self.assertEqual(defended["damage"], 0)
        self.assertEqual(guarded["health"], 1000)
        self.assertAlmostEqual(defended["hit_chance"], 0.50)

    def test_defense_expires_after_either_a_hit_or_a_miss(self):
        for first_roll in (0.10, 0.60):
            with self.subTest(first_roll=first_roll):
                attacker = draw_card("FireMage")
                opponent = draw_card("ShadowKnight")
                defend(opponent)
                with patch(
                    "world_model_starter.random.random", side_effect=[first_roll, 0.60]
                ):
                    first = attack(attacker, opponent, "GoldenHeart")
                    second = attack(attacker, opponent, "GoldenHeart")
                self.assertEqual(first["hit"], first_roll < 0.50)
                self.assertTrue(second["hit"])
                self.assertAlmostEqual(second["hit_chance"], 0.80)

    def test_repeated_defense_does_not_stack(self):
        attacker = draw_card("FireMage")
        opponent = draw_card("ShadowKnight")
        defend(opponent)
        defend(opponent)
        with patch("world_model_starter.random.random", return_value=0.40):
            result = attack(attacker, opponent, "GoldenHeart")
        self.assertTrue(result["hit"])
        self.assertAlmostEqual(result["hit_chance"], 0.50)

    def test_combat_does_not_change_other_draws_or_deck(self):
        attacker = draw_card("FireMage")
        opponent = draw_card("ShadowKnight")
        another_draw = draw_card("ShadowKnight")
        defend(opponent)
        with patch("world_model_starter.random.random", return_value=0.0):
            attack(attacker, opponent, "GoldenHeart")
        self.assertEqual(opponent["health"], 850)
        self.assertEqual(another_draw["health"], 1000)
        self.assertFalse(another_draw["defending"])
        self.assertEqual(DECK["ShadowKnight"]["health"], 1000)
        self.assertNotIn("defending", DECK["ShadowKnight"])

    def test_health_stops_at_zero_and_defeated_characters_cannot_act(self):
        attacker = draw_card("FireMage")
        opponent = draw_card("ShadowKnight")
        opponent["health"] = 10
        with patch("world_model_starter.random.random", return_value=0.0):
            result = attack(attacker, opponent, "GoldenHeart")
        self.assertEqual(result["damage"], 10)
        self.assertEqual(opponent["health"], 0)
        with self.assertRaises(ValueError):
            defend(opponent)
        with self.assertRaises(ValueError):
            attack(opponent, attacker, "Dark Blade Slash")
        with self.assertRaises(ValueError):
            attack(attacker, opponent, "GoldenHeart")


class TurnTests(unittest.TestCase):
    def test_card_selection_keeps_the_selected_copy_and_its_health(self):
        current = game.player("Ada")
        other = game.player("Bob")
        current.hand.append(draw_card("FireMage"))
        current.hand.append(draw_card("FireMage"))
        current.hand.append(draw_card("ShadowKnight"))
        current.hand[1]["health"] = 300

        with patch("builtins.input", side_effect=["wrong", "0", "4", "2"]):
            with redirect_stdout(io.StringIO()):
                game.choose_card(current)

        self.assertIs(current.active_card, current.hand[1])
        self.assertEqual(current.active_card["health"], 300)
        self.assertEqual(current.hand[0]["health"], 700)
        self.assertEqual(other.hand, [])

    def test_turn_retries_invalid_input_and_applies_defense_and_damage(self):
        current = game.player("Ada")
        other = game.player("Bob")
        current.active_card = draw_card("FireMage")
        other.active_card = draw_card("ShadowKnight")
        output = io.StringIO()

        with patch("builtins.input", side_effect=["wrong", "0"]):
            with redirect_stdout(output):
                game.take_turn(other, current)
        self.assertTrue(other.active_card["defending"])

        with patch(
            "builtins.input", side_effect=["wrong", "1", "wrong", "GoldenHeart"]
        ):
            with patch("world_model_starter.random.random", return_value=0.60):
                with redirect_stdout(output):
                    game.take_turn(current, other)
        self.assertEqual(other.active_card["health"], 1000)
        self.assertFalse(other.active_card["defending"])
        self.assertIn("miss", output.getvalue().lower())

        with patch("builtins.input", side_effect=["1", "GoldenHeart"]):
            with patch("world_model_starter.random.random", return_value=0.60):
                with redirect_stdout(output):
                    game.take_turn(current, other)
        self.assertEqual(other.active_card["health"], 850)
        self.assertEqual(current.active_card["health"], 700)
        self.assertIn("150", output.getvalue())
        self.assertIn("850", output.getvalue())

    def test_main_alternates_after_a_miss_and_stops_at_knockout(self):
        cards = [
            draw_card("FireMage"),
            draw_card("ShadowKnight"),
            draw_card("FireMage"),
            draw_card("ShadowKnight"),
            draw_card("FireMage"),
            draw_card("ShadowKnight"),
        ]
        cards[2]["health"] = 250
        cards[5]["health"] = 200
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
            with patch("world_model_starter.draw_card", side_effect=cards):
                with patch(
                    "world_model_starter.random.random", side_effect=[0.99, 0, 0, 0]
                ):
                    with redirect_stdout(output):
                        game.main()

        self.assertEqual(cards[2]["health"], 0)
        self.assertEqual(cards[5]["health"], 50)
        self.assertEqual(cards[0]["health"], 700)
        self.assertEqual(cards[1]["health"], 1000)
        self.assertEqual(cards[3]["health"], 1000)
        self.assertEqual(cards[4]["health"], 700)
        self.assertIn("Bob", output.getvalue().splitlines()[-1])


if __name__ == "__main__":
    unittest.main()
