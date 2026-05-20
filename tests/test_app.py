import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- GET /activities ---
def test_list_activities():
    # Arrange
    # (No setup needed for initial activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data  # Should not be empty

# --- POST /activities/{activity}/signup ---
def test_signup_participant():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Check participant is now in the list
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

# --- POST /activities/{activity}/unregister ---
def test_unregister_participant():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Ensure participant is signed up
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Check participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

# --- Edge case: duplicate signup ---
def test_duplicate_signup():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "duplicate@example.com"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code != 200
    data = response.json()
    assert "detail" in data

# --- Edge case: unregister non-existent participant ---
def test_unregister_nonexistent():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "notfound@example.com"

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code != 200
    data = response.json()
    assert "detail" in data
