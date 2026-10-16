import unittest
from datetime import date

from calories_app.db import Database
from calories_app.models import Dish, Entry
from calories_app.analyze import daily_totals, summary_for_day


class TestDailyTotals(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.dish = self.db.add_dish(
            Dish(name="Чизкейк", calories=387.4, protein=19.2, fat=2.26, carbs=4.98)
        )

    def tearDown(self):
        self.db.close()

    def test_empty_period_returns_zeros(self):
        result = daily_totals(self.db, date(2026, 5, 12), date(2026, 5, 14))
        self.assertEqual(len(result), 3)
        for day in result:
            self.assertEqual(day["calories"], 0)
            self.assertEqual(day["protein"], 0)

    def test_single_day_one_entry(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 12)))
        result = daily_totals(self.db, date(2026, 5, 12), date(2026, 5, 12))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["calories"], 387.4)
        self.assertEqual(result[0]["protein"], 19.2)

    def test_single_day_multiple_entries(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 12)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2026, 5, 12)))
        result = daily_totals(self.db, date(2026, 5, 12), date(2026, 5, 12))
        self.assertAlmostEqual(result[0]["calories"], 1162.2, places=1)
        self.assertAlmostEqual(result[0]["protein"], 57.6, places=1)

    def test_multiple_days(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 12)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2026, 5, 13)))
        result = daily_totals(self.db, date(2026, 5, 12), date(2026, 5, 13))
        self.assertEqual(result[0]["calories"], 387.4)
        self.assertAlmostEqual(result[1]["calories"], 774.8, places=1)

    def test_days_without_entries_are_zero(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 12)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 14)))
        result = daily_totals(self.db, date(2026, 5, 12), date(2026, 5, 14))
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]["calories"], 0)

    def test_start_after_end_raises(self):
        with self.assertRaises(ValueError):
            daily_totals(self.db, date(2026, 5, 16), date(2026, 5, 12))

    def test_result_is_ordered_by_date(self):
        result = daily_totals(self.db, date(2026, 5, 12), date(2026, 5, 16))
        dates = [d["date"] for d in result]
        self.assertEqual(dates, [
            date(2026, 5, 12),
            date(2026, 5, 13),
            date(2026, 5, 14),
            date(2026, 5, 15),
            date(2026, 5, 16),
        ])


class TestSummaryForDay(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.dish = self.db.add_dish(
            Dish(name="Чизкейк", calories=387.4, protein=19.2, fat=2.26, carbs=4.98)
        )

    def tearDown(self):
        self.db.close()

    def test_empty_day(self):
        result = summary_for_day(self.db, date(2026, 5, 12))
        self.assertEqual(result["calories"], 0)
        self.assertEqual(result["protein"], 0)
        self.assertEqual(result["fat"], 0)
        self.assertEqual(result["carbs"], 0)

    def test_single_entry(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 12)))
        result = summary_for_day(self.db, date(2026, 5, 12))
        self.assertEqual(result["calories"], 387.4)
        self.assertEqual(result["protein"], 19.2)

    def test_multiple_entries(self):
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=100, eaten_at=date(2026, 5, 12)))
        self.db.add_entry(Entry(dish_id=self.dish.id, grams=200, eaten_at=date(2026, 5, 12)))
        result = summary_for_day(self.db, date(2026, 5, 12))
        self.assertAlmostEqual(result["calories"], 1162.2, places=1)