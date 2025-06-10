import sqlalchemy.orm
from check_ins.repository import SqlCheckInRepository
from check_ins.service import CheckInService
from config import Config, register_routes
from db import Base
from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from habits.repository import SqlHabitRepository
from habits.service import HabitService
from injector import Binder


def create_app() -> Flask:
    conf = Config()

    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": [conf.frontend_url]}})

    register_routes(app)

    FlaskInjector(app, modules=[lambda binder: configure_dependencies(conf, binder)])

    return app


def configure_dependencies(config: Config, binder: Binder):
    engine = sqlalchemy.create_engine(config.db.url, echo=True)
    Base.metadata.create_all(engine)

    Session = sqlalchemy.orm.sessionmaker(engine)
    habit_repo = SqlHabitRepository(Session)
    check_in_repo = SqlCheckInRepository(Session)

    habit_service = HabitService(habit_repo, check_in_repo)
    check_in_service = CheckInService(check_in_repo, habit_repo)

    binder.bind(HabitService, to=habit_service)
    binder.bind(CheckInService, to=check_in_service)
