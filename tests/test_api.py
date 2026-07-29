from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Argus is running"
    }

def test_login():
    response = client.get("/login")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Login successful"
    }


def test_payment():
    response = client.get("/payment")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Payment failed"
    }


def test_database():
    response = client.get("/database")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Database down"
    }


def test_cache():
    response = client.get("/cache")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Cache miss"
    }