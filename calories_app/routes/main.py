from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/dishes")
def dishes():
    return render_template("dishes.html")


@bp.route("/diary")
def diary():
    return render_template("diary.html")


@bp.route("/analyze")
def analyze():
    return render_template("analyze.html")