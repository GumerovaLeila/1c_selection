from flask import Flask

from calories_app.db import Database


def create_app(db_path: str = "calories.db") -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-change-me"
    app.db = Database(db_path)
    from calories_app.routes import main
    app.register_blueprint(main.bp)
    from calories_app.routes import dishes as dishes_routes
    app.register_blueprint(dishes_routes.bp)
    from calories_app.routes import diary as diary_routes
    app.register_blueprint(diary_routes.bp)
    from calories_app.routes import analyze as analyze_routes
    app.register_blueprint(analyze_routes.bp)
    return app