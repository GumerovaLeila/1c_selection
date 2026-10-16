from calories_app.models import Dish

def calc_kbju(dish: Dish,  grams: float) -> dict:
    """
    Считает КБЖУ для порции блюда
    :param dish: блюдо
    :param grams: вес порции
    :return: словарь со значениями КБЖУ
    """

    coef = grams / 100.0
    return {
        "calories": round(dish.calories * coef, 2),
        "protein": round(dish.protein * coef, 2),
        "fat": round(dish.fat * coef, 2),
        "carbs": round(dish.carbs * coef, 2)
    }