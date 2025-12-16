"""Tests for unregister functionality"""
import pytest


def test_unregister_participant(client):
    """Test unregistering a participant"""
    email = "james@mergington.edu"
    response = client.delete(
        f"/activities/Basketball/unregister?email={email}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    assert "Basketball" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    email = "james@mergington.edu"
    client.delete(f"/activities/Basketball/unregister?email={email}")
    
    response = client.get("/activities")
    data = response.json()
    assert email not in data["Basketball"]["participants"]


def test_unregister_nonexistent_participant_fails(client):
    """Test that unregistering non-participant fails"""
    response = client.delete(
        "/activities/Basketball/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregistering from nonexistent activity fails"""
    response = client.delete(
        "/activities/Nonexistent/unregister?email=test@mergington.edu"
    )
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_then_unregister_cycle(client):
    """Test signing up and then unregistering"""
    email = "testcycle@mergington.edu"
    activity = "Basketball"
    
    # Sign up
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Verify signed up
    response_check1 = client.get("/activities")
    assert email in response_check1.json()[activity]["participants"]
    
    # Unregister
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 200
    
    # Verify unregistered
    response_check2 = client.get("/activities")
    assert email not in response_check2.json()[activity]["participants"]


def test_unregister_then_signup_again(client):
    """Test unregistering and signing up again"""
    email = "testresign@mergington.edu"
    activity = "Basketball"
    
    # Sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Unregister
    client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    
    # Verify signed up
    response_check = client.get("/activities")
    assert email in response_check.json()[activity]["participants"]
