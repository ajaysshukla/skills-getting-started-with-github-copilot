"""Tests for signup functionality"""
import pytest


def test_signup_new_participant(client):
    """Test signing up a new participant"""
    response = client.post(
        "/activities/Basketball/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]
    assert "Basketball" in data["message"]


def test_signup_adds_participant_to_list(client):
    """Test that signup actually adds the participant"""
    email = "newstudent@mergington.edu"
    client.post(f"/activities/Basketball/signup?email={email}")
    
    response = client.get("/activities")
    data = response.json()
    assert email in data["Basketball"]["participants"]


def test_signup_duplicate_fails(client):
    """Test that signing up twice fails"""
    email = "james@mergington.edu"  # Already signed up for Basketball
    response = client.post(f"/activities/Basketball/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "Already signed up" in data["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signing up for nonexistent activity fails"""
    response = client.post(
        "/activities/Nonexistent/signup?email=test@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_to_different_activities(client):
    """Test signing up to multiple different activities"""
    email = "multiactivity@mergington.edu"
    
    response1 = client.post(f"/activities/Basketball/signup?email={email}")
    assert response1.status_code == 200
    
    response2 = client.post(f"/activities/Tennis Club/signup?email={email}")
    assert response2.status_code == 200
    
    response = client.get("/activities")
    data = response.json()
    assert email in data["Basketball"]["participants"]
    assert email in data["Tennis Club"]["participants"]
