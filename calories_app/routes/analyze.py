from datetime import date, timedelta

from flask import Blueprint, render_template, jsonify, request, current_app

from calories_app.analyze import daily_totals

bp = Blueprint("analyze", __name__, url_prefix="/analyze")


@bp.route("/")
def analyze_page():
    return render_template("analyze.html")


@bp.route("/api/daily")
def api_daily():
    db = current_app.db
    days = int(request.args.get("days", 30))
    days = max(1, min(days, 365))

    end = date.today()
    start = end - timedelta(days=days - 1)

    data = daily_totals(db, start, end)
    return jsonify([
        {"date": d["date"].isoformat(), "calories": d["calories"]}
        for d in data
    ])