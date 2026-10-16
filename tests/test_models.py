import unittest
from datetime import date

from calories_app.models import Dish, Entry, Goals

class TestDish(unittest.TestCase):
    def test_valid_dish(self):
        dish = Dish(name="Чизкейк", calories=387.4, protein=19.2, fat=2.26, carbs=4.98)
        self.assertEqual(dish.name, "Чизкейк")
        self.assertEqual(dish.calories, 387.4)
        self.assertEqual(dish.protein, 19.2)
        self.assertEqual(dish.fat, 2.26)
        self.assertEqual(dish.carbs, 4.98)
        self.assertIsNone(dish.id)

    def test_empty_name(self):
        """Пустое название — ошибка"""
        with self.assertRaises(ValueError):
            Dish(name="", calories=100, protein=1, fat=1, carbs=1)

    def test_whitespace_name(self):
        """Название из пробелов — ошибка"""
        with self.assertRaises(ValueError):
            Dish(name="   ", calories=100, protein=1, fat=1, carbs=1)

    def test_negative_calories(self):
        """Отрицательные калории — ошибка"""
        with self.assertRaises(ValueError):
            Dish(name="Тест", calories=-1, protein=1, fat=1, carbs=1)

    def test_negative_protein(self):
        """Отрицательные белки — ошибка"""
        with self.assertRaises(ValueError):
            Dish(name="Тест", calories=100, protein=-1, fat=1, carbs=1)

    def test_negative_fat(self):
        """Отрицательные жиры — ошибка"""
        with self.assertRaises(ValueError):
            Dish(name="Тест", calories=100, protein=1, fat=-1, carbs=1)

    def test_negative_carbs(self):
        """Отрицательные углеводы — ошибка"""
        with self.assertRaises(ValueError):
            Dish(name="Тест", calories=100, protein=1, fat=1, carbs=-1)

class TestEntry(unittest.TestCase):
    def test_valid_entry(self):
        entry = Entry(dish_id=1, grams=200, eaten_at=date(2025, 1, 15))
        self.assertEqual(entry.dish_id, 1)
        self.assertEqual(entry.grams, 200)
        self.assertEqual(entry.eaten_at, date(2025, 1, 15))
        self.assertIsNone(entry.id)

    def test_zero_grams(self):
        """Ноль грамм — ошибка"""
        with self.assertRaises(ValueError):
            Entry(dish_id=1, grams=0, eaten_at=date(2025, 1, 15))

    def test_negative_grams(self):
        """Отрицательный вес — ошибка"""
        with self.assertRaises(ValueError):
            Entry(dish_id=1, grams=-50, eaten_at=date(2025, 1, 15))

class TestGoals(unittest.TestCase):
    def test_valid_goals(self):
        goals = Goals(calories=2500, protein=150, fat=80, carbs=300)
        self.assertEqual(goals.calories, 2500)
        self.assertEqual(goals.protein, 150)
        self.assertEqual(goals.fat, 80)
        self.assertEqual(goals.carbs, 300)

    def test_negative_calories(self):
        """Отрицательные калории — ошибка"""
        with self.assertRaises(ValueError):
            Goals(calories=-1, protein=150, fat=80, carbs=300)

    def test_negative_protein(self):
        """Отрицательные белки — ошибка"""
        with self.assertRaises(ValueError):
            Goals(calories=2500, protein=-1, fat=80, carbs=300)

    def test_negative_fat(self):
        """Отрицательные жиры — ошибка"""
        with self.assertRaises(ValueError):
            Goals(calories=2500, protein=150, fat=-1, carbs=300)

    def test_negative_carbs(self):
        """Отрицательные углеводы — ошибка"""
        with self.assertRaises(ValueError):
            Goals(calories=2500, protein=150, fat=80, carbs=-1)