from flask.testing import FlaskClient

"""Integration tests for the habit routes. These tests assume that the database
is empty before each test run. The database is mocked using an in-memory
database, but apart from that, the test run against the actual application,
including the routes and the service layer."""


def test_get_all_habits__given_no_habits_exist__returns_empty_list(client: FlaskClient):
    response = client.get("/habits")
    assert response.status_code == 200
    assert response.json == []


def test_get_all_habits__given_a_habits_created__returns_list_with_that_habit(
    client: FlaskClient,
):
    # Create a habit first
    response = client.post("/habits", json={"description": "Test Habit"})
    assert response.status_code == 201
    created_habit = response.json

    # Now get all habits
    response = client.get("/habits")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == created_habit["id"]
    assert response.json[0]["description"] == "Test Habit"


def test_get_all_habits__given_multiple_habits_created__returns_list_with_all_habits(
    client: FlaskClient,
):
    # Create multiple habits
    response1 = client.post("/habits", json={"description": "First Habit"})
    assert response1.status_code == 201
    habit1 = response1.json

    response2 = client.post("/habits", json={"description": "Second Habit"})
    assert response2.status_code == 201
    habit2 = response2.json

    # Now get all habits
    response = client.get("/habits")
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] == habit1["id"]
    assert response.json[0]["description"] == "First Habit"
    assert response.json[1]["id"] == habit2["id"]
    assert response.json[1]["description"] == "Second Habit"


def test_get_habit__given_non_existent_id__returns_404(
    client: FlaskClient,
):
    response = client.get("/habits/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 404
    assert response.json["error"] == "habit not found"


def test_get_habit__given_valid_id__returns_habit(
    client: FlaskClient,
):
    # Create a habit first
    response = client.post("/habits", json={"description": "Test Habit"})
    assert response.status_code == 201
    created_habit = response.json

    # Now get the habit by ID
    response = client.get(f"/habits/{created_habit['id']}")
    assert response.status_code == 200
    assert response.json["id"] == created_habit["id"]
    assert response.json["description"] == "Test Habit"


def test_put_habit__given_valid_id_and_data__updates_habit(
    client: FlaskClient,
):
    # Create a habit first
    response = client.post("/habits", json={"description": "Test Habit"})
    assert response.status_code == 201
    created_habit = response.json

    # Update the habit
    updated_data = {"description": "Updated Habit"}
    response = client.put(f"/habits/{created_habit['id']}", json=updated_data)
    assert response.status_code == 204

    # Verify the update
    response = client.get(f"/habits/{created_habit['id']}")
    assert response.status_code == 200
    assert response.json["description"] == "Updated Habit"

    response = client.get("/habits")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["id"] == created_habit["id"]
    assert response.json[0]["description"] == "Updated Habit"


def test_delete_habit__given_valid_id__deletes_habit(
    client: FlaskClient,
):
    # Create a habit first
    response = client.post("/habits", json={"description": "Test Habit"})
    assert response.status_code == 201
    created_habit = response.json

    # Delete the habit
    response = client.delete(f"/habits/{created_habit['id']}")
    assert response.status_code == 204

    # Verify the deletion
    response = client.get(f"/habits/{created_habit['id']}")
    assert response.status_code == 404

    response = client.get("/habits")
    assert response.status_code == 200
    assert len(response.json) == 0
