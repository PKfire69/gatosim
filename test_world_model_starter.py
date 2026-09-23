import unittest
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
