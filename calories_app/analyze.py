from datetime import date, timedelta

from calories_app.db import Database
from calories_app.calculation import calc_kbju


def daily_totals(db: Database, start: date, end: date) -> list[dict]:
    """Статистика по дням"""
    if start > end:
        raise ValueError("start не может быть позже end")

    totals: dict[date, dict] = {}
    current = start
    while current <= end:
        totals[current] = {
            "date": current,
            "calories": 0.0,
            "protein": 0.0,
            "fat": 0.0,
            "carbs": 0.0,
        }
        current += timedelta(days=1)

    entries = db.get_entries_in_range(start, end)

    for entry in entries:
        dish = db.get_dish(entry.dish_id)
        kbju = calc_kbju(dish, entry.grams)
        day = totals[entry.eaten_at]
        day["calories"] += kbju["calories"]
        day["protein"] += kbju["protein"]
        day["fat"] += kbju["fat"]
        day["carbs"] += kbju["carbs"]

    return [totals[start + timedelta(days=i)]
            for i in range((end - start).days + 1)]


def summary_for_day(db: Database, day: date) -> dict:
    """Сводка за один день: сколько всего съедено"""
    entries = db.get_entries_by_date(day)
    total = {"calories": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}

    for entry in entries:
        dish = db.get_dish(entry.dish_id)
        if dish is None:
            continue
        kbju = calc_kbju(dish, entry.grams)
        for key in total:
            total[key] += kbju[key]

    return total