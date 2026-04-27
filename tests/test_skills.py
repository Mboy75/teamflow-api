from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_skills():
    response = client.get("/skills/")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert "items" in data
    assert isinstance(data["items"], list)