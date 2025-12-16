"""Tests for the activities endpoints"""
import pytest


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "Tennis Club" in data
    assert len(data) == 9


def test_get_activities_has_correct_structure(client):
    """Test that activities have correct structure"""
    response = client.get("/activities")
    data = response.json()
    
    activity = data["Basketball"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_includes_initial_participants(client):
    """Test that activities include initial participants"""
    response = client.get("/activities")
    data = response.json()
    
    assert "james@mergington.edu" in data["Basketball"]["participants"]
    assert "alex@mergington.edu" in data["Tennis Club"]["participants"]
