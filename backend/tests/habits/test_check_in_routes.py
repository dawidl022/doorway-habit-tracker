import datetime
from uuid import UUID

from flask.testing import FlaskClient

"""Integration tests for the check-in routes. See documentation in
test_habit_routes.py for more details."""


def test_get_check_ins__given_invalid_habit_id__returns_404(
    client: FlaskClient,
):
    response = client.get("/habits/123e4567-e89b-12d3-a456-426614174000/check-ins")
    assert response.status_code == 404
    assert response.json["error"] == "habit not found"


def test_get_check_ins__given_no_check_ins_exist__returns_empty_list(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    # Now get check-ins for that habit
    response = client.get(f"/habits/{created_habit_id}/check-ins")
    assert response.status_code == 200
    assert response.json == []


def test_get_check_ins__given_check_ins_exist__returns_list_of_check_ins(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    # Create a check-in for the habit
    response = client.put(
        f"/habits/{created_habit_id}/check-ins", json={"date": "2023-10-01"}
    )
    assert response.status_code == 204

    # Now get check-ins for that habit
    response = client.get(f"/habits/{created_habit_id}/check-ins")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["date"] == "2023-10-01"


def test_check_in__given_invalid_habit_id__returns_404(
    client: FlaskClient,
):
    response = client.put(
        "/habits/123e4567-e89b-12d3-a456-426614174000/check-ins",
        json={"date": "2023-10-01"},
    )
    assert response.status_code == 404
    assert response.json["error"] == "habit not found"


def test_check_in__given_date_in_future__returns_400(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    today = datetime.date.today()
    # Add two days to avoid edge case where date changes during the test
    future = today + datetime.timedelta(days=2)

    # Attempt to check in with a future date
    response = client.put(
        f"/habits/{created_habit_id}/check-ins", json={"date": future.isoformat()}
    )
    assert response.status_code == 400
    assert response.json["error"] == "date cannot be in the future"


def test_delete_check_in__given_invalid_habit_id__returns_404(
    client: FlaskClient,
):
    response = client.delete(
        "/habits/123e4567-e89b-12d3-a456-426614174000/check-ins",
        json={"date": "2023-10-01"},
    )
    assert response.status_code == 404
    assert response.json["error"] == "habit not found"


def test_delete_check_in__given_no_check_in_exists__returns_204(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    # Attempt to delete a check-in that doesn't exist
    response = client.delete(
        f"/habits/{created_habit_id}/check-ins", json={"date": "2023-10-01"}
    )
    assert response.status_code == 204


def test_delete_check_in__given_check_in_exists__deletes_check_in(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    # Create a check-in for the habit
    response = client.put(
        f"/habits/{created_habit_id}/check-ins", json={"date": "2023-10-01"}
    )
    assert response.status_code == 204

    # Now delete the check-in
    response = client.delete(
        f"/habits/{created_habit_id}/check-ins", json={"date": "2023-10-01"}
    )
    assert response.status_code == 204

    # Verify the check-in was deleted
    response = client.get(f"/habits/{created_habit_id}/check-ins")
    assert response.status_code == 200
    assert response.json == []


def test_get_all_habits__given_habit_not_checked_in_today__returns_completed_today_false(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    # Get all habits
    response = client.get("/habits")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == created_habit_id
    assert response.json[0]["completedToday"] is False


def test_get_all_habits__given_habit_checked_in_today__returns_completed_today_true(
    client: FlaskClient,
):
    created_habit_id = create_test_habit(client)

    # Check in for today
    today = datetime.date.today()
    response = client.put(
        f"/habits/{created_habit_id}/check-ins", json={"date": today.isoformat()}
    )
    assert response.status_code == 204

    # Get all habits
    response = client.get("/habits")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == created_habit_id
    assert response.json[0]["completedToday"] is True


def create_test_habit(client: FlaskClient) -> UUID:
    response = client.post("/habits", json={"description": "Test Habit"})
    assert response.status_code == 201
    created_habit = response.json
    return created_habit["id"]
