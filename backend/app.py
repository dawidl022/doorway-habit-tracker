from http import HTTPStatus

from flask import Flask, jsonify, request
from habits import dtos
from habits import service as habits

app = Flask(__name__)

ALL_HABITS_ENDPOINT = "/habits"
HABIT_ENDPOINT = f"/{ALL_HABITS_ENDPOINT}/<id>"


@app.get(ALL_HABITS_ENDPOINT)
def get_all_habits(habits_service: habits.HabitService):
    return jsonify(habits_service.get_all())


@app.get(HABIT_ENDPOINT)
def get_habit(id: str, habits_service: habits.HabitService):
    return jsonify(habits_service.get(id))


@app.post(ALL_HABITS_ENDPOINT)
def create_habit(habits_service: habits.HabitService):
    created_habit = habits_service.create(dtos.NewHabit.from_dict(request.json))
    return jsonify(created_habit.to_dict()), HTTPStatus.CREATED


@app.put(HABIT_ENDPOINT)
def update_habit(id: str, habits_service: habits.HabitService):
    habits_service.update(id, dtos.NewHabit.from_dict(request.json))


@app.delete(
    HABIT_ENDPOINT,
)
def delete_habit(id: str, habits_service: habits.HabitService):
    habits_service.delete(id)
