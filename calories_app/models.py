from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

@dataclass
class Dish:
    """Сохраненное блюда, с КБЖУ на 100 грамм"""
    name: str
    calories: float
    protein: float
    fat: float
    carbs: float
    id: Optional[int] = None # id в БД, если не сохранено, то None

    def __post_init__(self):
        """Немного проверок на корректность"""
        if not self.name.strip():
            raise ValueError("Название блюда не может быть пустым")
        if any(count < 0 for count in (self.calories, self.protein, self.fat, self.carbs)):
            raise ValueError("КБЖУ  должно быть неотрицательным")

@dataclass
class Entry:
    """Записи о съеденном блюде с датой"""
    dish_id: int
    grams: float
    eaten_at: date
    id: Optional[int] = None

    def __post_init__(self):
        """Проверка на корректность"""
        if self.grams <= 0:
            raise ValueError("Вес порции должен быть положителен")

@dataclass
class Goals:
    """Цели пользователя по КБЖУ"""
    calories: float
    protein: float
    fat: float
    carbs: float

    def __post_init__(self):
        """Проверка на корректность"""
        for name, value in (
                ("calories", self.calories),
                ("protein", self.protein),
                ("fat", self.fat),
                ("carbs", self.carbs),
        ):
            if value < 0:
                raise ValueError(f"Цель {name} не может быть отрицательной")