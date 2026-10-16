from datetime import date

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from calories_app.models import Entry

bp = Blueprint("diary", __name__, url_prefix="/diary")


@bp.route("/")
def list_entries():
    db = current_app.db

    date_str = request.args.get("date")
    try:
        day = date.fromisoformat(date_str) if date_str else date.today()
    except ValueError:
        day = date.today()

    entries = db.get_entries_by_date(day)
    dishes = db.get_all_dishes()

    rows = []
    totals = {"calories": 0.0, "protein": 0.0, "fat": 0.0, "carbs": 0.0}
    for e in entries:
        dish = db.get_dish(e.dish_id)
        if dish is None:
            continue
        from calories_app.calculation import calc_kbju
        kbju = calc_kbju(dish, e.grams)
        rows.append({"entry": e, "dish": dish, "kbju": kbju})
        for k in totals:
            totals[k] += kbju[k]

    return render_template(
        "diary.html",
        rows=rows,
        dishes=dishes,
        day=day,
        totals=totals,
    )


@bp.route("/add", methods=["POST"])
def add_entry():
    db = current_app.db
    try:
        dish_id = int(request.form["dish_id"])
        grams = float(request.form["grams"])
        eaten_at = date.fromisoformat(request.form["eaten_at"])

        entry = Entry(dish_id=dish_id, grams=grams, eaten_at=eaten_at)
        db.add_entry(entry)
        flash("Запись добавлена", "success")
        return redirect(url_for("diary.list_entries", date=eaten_at.isoformat()))
    except (ValueError, KeyError) as e:
        flash(f"Ошибка: {e}", "danger")
        return redirect(url_for("diary.list_entries"))


@bp.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    db = current_app.db
    entry = db.get_entry(entry_id)
    if entry:
        db.delete_entry(entry_id)
        flash("Запись удалена", "success")
        return redirect(url_for("diary.list_entries", date=entry.eaten_at.isoformat()))
    return redirect(url_for("diary.list_entries"))