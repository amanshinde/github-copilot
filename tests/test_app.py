"""Test suite for Mergington High School API"""
import pytest


def test_root_redirect(client):
    """Test GET / redirects to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9


def test_get_activities_structure(client):
    """Test that activities have required fields"""
    response = client.get("/activities")
    data = response.json()
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_signup_for_activity_success(client):
    """Test successful signup for an activity"""
    response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_signed_up(client):
    """Test signup when student is already registered"""
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_remove_participant_success(client):
    """Test successful removal of a participant"""
    # First signup
    client.post("/activities/Chess Club/signup?email=temp@mergington.edu")
    # Then remove
    response = client.delete("/activities/Chess Club/participants/temp@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]
    assert "temp@mergington.edu" in data["message"]


def test_remove_participant_activity_not_found(client):
    """Test removal from non-existent activity"""
    response = client.delete("/activities/Nonexistent Activity/participants/test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_remove_participant_not_found(client):
    """Test removal of participant not in activity"""
    response = client.delete("/activities/Chess Club/participants/notinactivity@mergington.edu")
    assert response.status_code == 400
    assert "Participant not found" in response.json()["detail"]