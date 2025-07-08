import io
from unittest import mock

from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def get_token():
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    return response.json()["access_token"]


def test_csv_plugin_run(tmp_path):
    token = get_token()
    file_content = b"name,age\nJohn,22\nJane,24"
    response = client.post(
        "/run-plugin",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", io.BytesIO(file_content), "text/csv")},
        data={"plugin_type": "csv"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert data["download_url"].endswith(".xlsx")
