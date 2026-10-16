import unittest

from calories_app.models import Dish
from calories_app.calculation import calc_kbju

class TestCalcKbju(unittest.TestCase):
    def setUp(self):
        """Блюдо, используемое в тесте"""
        self.dish = Dish(
            name="Чизкейк шоколадный",
            calories=387.4,
            protein=19.2,
            fat=2.26,
            carbs=4.98
        )

    def test_100_grams(self):
        result = calc_kbju(self.dish, 100)
        self.assertEqual(result["calories"], 387.4)
        self.assertEqual(result["protein"], 19.2)
        self.assertEqual(result["fat"], 2.26)
        self.assertEqual(result["carbs"], 4.98)

    def test_200_grams(self):
        result = calc_kbju(self.dish, 200)
        self.assertEqual(result["calories"], 774.8)
        self.assertEqual(result["protein"], 38.4)
        self.assertEqual(result["fat"], 4.52)
        self.assertEqual(result["carbs"], 9.96)

    def test_50_grams(self):
        result = calc_kbju(self.dish, 50)
        self.assertEqual(result["calories"], 193.7)
        self.assertEqual(result["protein"], 9.6)
        self.assertEqual(result["fat"], 1.13)
        self.assertEqual(result["carbs"], 2.49)