import unittest
from datetime import date

from calories_app.db import Database
from calories_app.models import Dish, Entry, Goals


class TestDatabaseDishes(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.dish = Dish(name="Чизкейк", calories=387.4, protein=19.2, fat=2.26, carbs=4.98)

    def tearDown(self):
        self.db.close()

    def test_add_dish_assigns_id(self):
        saved = self.db.add_dish(self.dish)
        self.assertIsNotNone(saved.id)
        self.assertEqual(saved.id, 1)

    def test_get_dish(self):
        saved = self.db.add_dish(self.dish)
        fetched = self.db.get_dish(saved.id)
        self.assertEqual(fetched.name, "Чизкейк")
        self.assertEqual(fetched.calories, 387.4)

    def test_get_dish_not_found(self):
        self.assertIsNone(self.db.get_dish(999))

    def test_get_all_dishes_sorted(self):
        self.db.add_dish(Dish(name="Банан", calories=89, protein=1.1, fat=0.3, carbs=23))
        self.db.add_dish(Dish(name="Яблоко", calories=52, protein=0.3, fat=0.2, carbs=14))
        self.db.add_dish(Dish(name="Апельсин", calories=47, protein=0.9, fat=0.1, carbs=12))
        names = [d.name for d in self.db.get_all_dishes()]
        self.assertEqual(names, ["Апельсин", "Банан", "Яблоко"])

    def test_search_dishes(self):
        self.db.add_dish(Dish(name="Чизкейк шоколадный", calories=387, protein=19, fat=2, carbs=5))
        self.db.add_dish(Dish(name="Чизкейк ванильный", calories=350, protein=15, fat=3, carbs=6))
        self.db.add_dish(Dish(name="Банан", calories=89, protein=1, fat=0, carbs=23))
        results = self.db.search_dishes("Чизкейк")
        self.assertEqual(len(results), 2)

    def test_update_dish(self):
        saved = self.db.add_dish(self.dish)
        saved.calories = 400
        self.db.update_dish(saved)
        fetched = self.db.get_dish(saved.id)
        self.assertEqual(fetched.calories, 400)

    def test_update_dish_without_id(self):
        dish_without_id = Dish(name="Тест", calories=1, protein=1, fat=1, carbs=1)
        with self.assertRaises(ValueError):
            self.db.update_dish(dish_without_id)

    def test_delete_dish(self):
        saved = self.db.add_dish(self.dish)
        self.db.delete_dish(saved.id)
        self.assertIsNone(self.db.get_dish(saved.id))


class TestDatabaseEntries(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.dish = self.db.add_dish(
            Dish(name="Чизкейк", calories=387, protein=19, fat=2, carbs=5)
        )

    def tearDown(self):
        self.db.close()

    def test_add_entry_assigns_id(self):
        entry = Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2025, 1, 15))
        saved = self.db.add_entry(entry)
        self.assertEqual(saved.id, 1)

    def test_get_entry(self):
        entry = Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2025, 1, 15))
        saved = self.db.add_entry(entry)
        fetched = self.db.get_entry(saved.id)
        self.assertEqual(fetched.grams, 200)
        self.assertEqual(fetched.eaten_at, date(2025, 1, 15))

    def test_get_entries_by_date(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2025, 1, 15)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=150, eaten_at=date(2025, 1, 15)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2025, 1, 16)))
        entries = self.db.get_entries_by_date(date(2025, 1, 15))
        self.assertEqual(len(entries), 2)

    def test_get_entries_in_range(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2025, 1, 10)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2025, 1, 15)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2025, 1, 20)))
        entries = self.db.get_entries_in_range(date(2025, 1, 12), date(2025, 1, 18))
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].eaten_at, date(2025, 1, 15))

    def test_delete_entry(self):
        entry = self.db.add_entry(
            Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2025, 1, 15))
        )
        self.db.delete_entry(entry.id)
        self.assertIsNone(self.db.get_entry(entry.id))

    def test_cascade_delete_dish(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2025, 1, 15)))
        self.db.delete_dish(self.dish.id)
        self.assertEqual(len(self.db.get_entries_by_date(date(2025, 1, 15))), 0)


class TestDatabaseGoals(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")

    def tearDown(self):
        self.db.close()

    def test_get_goals_when_empty(self):
        self.assertIsNone(self.db.get_goals())

    def test_save_and_get_goals(self):
        self.db.save_goals(Goals(calories=2500, protein=150, fat=80, carbs=300))
        g = self.db.get_goals()
        self.assertEqual(g.calories, 2500)
        self.assertEqual(g.protein, 150)

    def test_save_goals_overwrites(self):
        self.db.save_goals(Goals(calories=2500, protein=150, fat=80, carbs=300))
        self.db.save_goals(Goals(calories=2000, protein=120, fat=70, carbs=250))
        g = self.db.get_goals()
        self.assertEqual(g.calories, 2000)