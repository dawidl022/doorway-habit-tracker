import sqlalchemy.orm
from check_ins.repository import SqlCheckInRepository
from check_ins.routes import bp as check_ins_bp
from check_ins.service import CheckInService
from config import DbConfig
from db import Base
from flask import Flask
from flask_injector import FlaskInjector
from habits.repository import SqlHabitRepository
from habits.routes import bp as habits_bp
from habits.service import HabitService
from injector import Binder
from validation import HabitNotFoundError, ValidationError


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(habits_bp)
    app.register_blueprint(check_ins_bp)
    app.register_error_handler(ValidationError, ValidationError.handle)
    app.register_error_handler(HabitNotFoundError, HabitNotFoundError.handle)

    FlaskInjector(app, modules=[configure_dependencies])

    return app


def configure_dependencies(binder: Binder):
    db_config = DbConfig()
    engine = sqlalchemy.create_engine(db_config.url, echo=True)
    Base.metadata.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker(engine)
    habit_repo = SqlHabitRepository(Session)
    habit_service = HabitService(habit_repo)

    check_in_repo = SqlCheckInRepository(Session)
    check_in_service = CheckInService(check_in_repo, habit_repo)

    binder.bind(HabitService, to=habit_service)
    binder.bind(CheckInService, to=check_in_service)
