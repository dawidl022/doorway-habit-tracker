from http import HTTPStatus

from flask import Blueprint, jsonify, request
from validation import HabitNotFoundError, validate_uuid

from . import dtos
from .service import HabitService

bp = Blueprint("habits", __name__, url_prefix="/habits")

HABIT_ENDPOINT = f"/<id>"


@bp.get("")
def get_all_habits(habits_service: HabitService):
    return jsonify(habits_service.get_all())


@bp.get(HABIT_ENDPOINT)
def get_habit(id: str, habits_service: HabitService):
    id = validate_uuid(id)
    habit = habits_service.get(id)
    if habit is None:
        raise HabitNotFoundError()
    return jsonify(habit)


@bp.post("")
def create_habit(habits_service: HabitService):
    created_habit = habits_service.create(dtos.NewHabit.from_dict(request.json))
    return jsonify(created_habit.to_dict()), HTTPStatus.CREATED


@bp.put(HABIT_ENDPOINT)
def update_habit(id: str, habits_service: HabitService):
    id = validate_uuid(id)
    habits_service.update(id, dtos.NewHabit.from_dict(request.json))
    return "", HTTPStatus.NO_CONTENT


@bp.delete(HABIT_ENDPOINT)
def delete_habit(id: str, habits_service: HabitService):
    id = validate_uuid(id)
    habits_service.delete(id)
    return "", HTTPStatus.NO_CONTENT


# TODO route handler tests:
# - invalid UUIDs
# - invalid Habit DTOs
# - no Habit returns 404
