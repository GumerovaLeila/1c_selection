from flask import Blueprint, render_template, request, redirect, url_for, flash

from calories_app.models import Dish

bp = Blueprint("dishes", __name__, url_prefix="/dishes")


def _get_db():
    from flask import current_app
    return current_app.db

@bp.route("/")
def list_dishes():
    db = _get_db()
    query = request.args.get("q", "").strip()
    edit_id = request.args.get("edit", type=int)

    dishes = db.search_dishes(query) if query else db.get_all_dishes()
    edit_dish = db.get_dish(edit_id) if edit_id else None

    return render_template(
        "dishes.html",
        dishes=dishes,
        query=query,
        edit_dish=edit_dish,
    )


@bp.route("/add", methods=["POST"])
def add_dish():
    db = _get_db()
    try:
        dish = Dish(
            name=request.form["name"].strip(),
            calories=float(request.form["calories"]),
            protein=float(request.form["protein"]),
            fat=float(request.form["fat"]),
            carbs=float(request.form["carbs"]),
        )
        db.add_dish(dish)
        flash(f"Блюдо «{dish.name}» добавлено", "success")
    except (ValueError, KeyError) as e:
        flash(f"Ошибка: {e}", "danger")
    return redirect(url_for("dishes.list_dishes"))


@bp.route("/update/<int:dish_id>", methods=["POST"])
def update_dish(dish_id):
    db = _get_db()
    try:
        dish = Dish(
            id=dish_id,
            name=request.form["name"].strip(),
            calories=float(request.form["calories"]),
            protein=float(request.form["protein"]),
            fat=float(request.form["fat"]),
            carbs=float(request.form["carbs"]),
        )
        db.update_dish(dish)
        flash(f"Блюдо «{dish.name}» обновлено", "success")
    except (ValueError, KeyError) as e:
        flash(f"Ошибка: {e}", "danger")
    return redirect(url_for("dishes.list_dishes"))


@bp.route("/delete/<int:dish_id>", methods=["POST"])
def delete_dish(dish_id):
    db = _get_db()
    dish = db.get_dish(dish_id)
    if dish:
        db.delete_dish(dish_id)
        flash(f"Блюдо «{dish.name}» удалено", "success")
    return redirect(url_for("dishes.list_dishes"))