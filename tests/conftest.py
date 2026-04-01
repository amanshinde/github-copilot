"""Pytest configuration and fixtures"""
import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI application"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state after each test"""
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)