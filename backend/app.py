from config import DbConfig
from flask import Flask
from flask_injector import FlaskInjector
from habits.repository import SqlHabitRepository
from habits.routes import bp as habits_bp
from habits.service import HabitService
from injector import Binder


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(habits_bp)

    FlaskInjector(app, modules=[configure_dependencies])

    return app


def configure_dependencies(binder: Binder):
    habit_repo = SqlHabitRepository(DbConfig())
    habit_service = HabitService(habit_repo)

    binder.bind(HabitService, to=habit_service)
