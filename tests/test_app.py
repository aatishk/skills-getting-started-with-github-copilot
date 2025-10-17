
import pytest
from fastapi.testclient import TestClient
from src.app import app, get_initial_activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    app.state.activities = get_initial_activities()


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Try signing up again (should fail)
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400


def test_unregister_from_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Sign up first
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]
    # Try unregistering again (should fail)
    response2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 400


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_invalid_activity():
    response = client.post("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
