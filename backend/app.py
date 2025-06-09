from flask import Flask, jsonify, request
from habits import dtos
from habits import service as habits

app = Flask(__name__)

ALL_HABITS_ENDPOINT = "/habits"
HABIT_ENDPOINT = f"/{ALL_HABITS_ENDPOINT}/<id>"


@app.get(ALL_HABITS_ENDPOINT)
def get_all_habits():
    return jsonify(habits.get_all())


@app.get(HABIT_ENDPOINT)
def get_habit(id: str):
    return jsonify(habits.get(id))


@app.post(ALL_HABITS_ENDPOINT)
def create_habit():
    habits.create(dtos.NewHabit.from_dict(request.json))


@app.put(HABIT_ENDPOINT)
def update_habit(id: str):
    habits.update(id, dtos.NewHabit.from_dict(request.json))


@app.delete(HABIT_ENDPOINT)
def delete_habit(id: str):
    habits.delete(id)
