import sqlite3
from datetime import date
from typing import Optional

from calories_app.models import Dish, Entry, Goals


SCHEMA = """
CREATE TABLE IF NOT EXISTS dishes (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL,
    calories REAL    NOT NULL,
    protein  REAL    NOT NULL,
    fat      REAL    NOT NULL,
    carbs    REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS entries (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    dish_id  INTEGER NOT NULL,
    grams    REAL    NOT NULL,
    eaten_at TEXT    NOT NULL,
    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goals (
    id       INTEGER PRIMARY KEY CHECK (id = 1),
    calories REAL NOT NULL,
    protein  REAL NOT NULL,
    fat      REAL NOT NULL,
    carbs    REAL NOT NULL
);
"""


class Database:
    def __init__(self, path: str = "calories.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()


    def add_dish(self, dish: Dish) -> Dish:
        cur = self.conn.execute(
            "INSERT INTO dishes (name, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?)",
            (dish.name, dish.calories, dish.protein, dish.fat, dish.carbs),
        )
        self.conn.commit()
        dish.id = cur.lastrowid
        return dish

    def get_dish(self, dish_id: int) -> Optional[Dish]:
        row = self.conn.execute(
            "SELECT * FROM dishes WHERE id = ?", (dish_id,)
        ).fetchone()
        return self._row_to_dish(row) if row else None

    def get_all_dishes(self) -> list[Dish]:
        rows = self.conn.execute(
            "SELECT * FROM dishes ORDER BY name"
        ).fetchall()
        return [self._row_to_dish(r) for r in rows]

    def search_dishes(self, query: str) -> list[Dish]:
        rows = self.conn.execute(
            "SELECT * FROM dishes WHERE name LIKE ? ORDER BY name",
            (f"%{query}%",),
        ).fetchall()
        return [self._row_to_dish(r) for r in rows]

    def update_dish(self, dish: Dish) -> None:
        if dish.id is None:
            raise ValueError("Нельзя обновить блюдо без id")
        self.conn.execute(
            "UPDATE dishes SET name=?, calories=?, protein=?, fat=?, carbs=? WHERE id=?",
            (dish.name, dish.calories, dish.protein, dish.fat, dish.carbs, dish.id),
        )
        self.conn.commit()

    def delete_dish(self, dish_id: int) -> None:
        self.conn.execute("DELETE FROM dishes WHERE id = ?", (dish_id,))
        self.conn.commit()

    @staticmethod
    def _row_to_dish(row: sqlite3.Row) -> Dish:
        return Dish(
            id=row["id"],
            name=row["name"],
            calories=row["calories"],
            protein=row["protein"],
            fat=row["fat"],
            carbs=row["carbs"],
        )

    def add_entry(self, entry: Entry) -> Entry:
        cur = self.conn.execute(
            "INSERT INTO entries (dish_id, grams, eaten_at) VALUES (?, ?, ?)",
            (entry.dish_id, entry.grams, entry.eaten_at.isoformat()),
        )
        self.conn.commit()
        entry.id = cur.lastrowid
        return entry

    def get_entry(self, entry_id: int) -> Optional[Entry]:
        row = self.conn.execute(
            "SELECT * FROM entries WHERE id = ?", (entry_id,)
        ).fetchone()
        return self._row_to_entry(row) if row else None

    def get_entries_by_date(self, day: date) -> list[Entry]:
        rows = self.conn.execute(
            "SELECT * FROM entries WHERE eaten_at = ? ORDER BY id",
            (day.isoformat(),),
        ).fetchall()
        return [self._row_to_entry(r) for r in rows]

    def get_entries_in_range(self, start: date, end: date) -> list[Entry]:
        rows = self.conn.execute(
            "SELECT * FROM entries WHERE eaten_at BETWEEN ? AND ? ORDER BY eaten_at, id",
            (start.isoformat(), end.isoformat()),
        ).fetchall()
        return [self._row_to_entry(r) for r in rows]

    def delete_entry(self, entry_id: int) -> None:
        self.conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
        self.conn.commit()

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> Entry:
        return Entry(
            id=row["id"],
            dish_id=row["dish_id"],
            grams=row["grams"],
            eaten_at=date.fromisoformat(row["eaten_at"]),
        )

    def save_goals(self, goals: Goals) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO goals (id, calories, protein, fat, carbs) VALUES (1, ?, ?, ?, ?)",
            (goals.calories, goals.protein, goals.fat, goals.carbs),
        )
        self.conn.commit()

    def get_goals(self) -> Optional[Goals]:
        row = self.conn.execute("SELECT * FROM goals WHERE id = 1").fetchone()
        if not row:
            return None
        return Goals(
            calories=row["calories"],
            protein=row["protein"],
            fat=row["fat"],
            carbs=row["carbs"],
        )