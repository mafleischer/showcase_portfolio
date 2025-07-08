from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post("/token", data={"username": "admin", "password": "wrong"})
    assert response.status_code == 400
