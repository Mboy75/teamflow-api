from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_token():
    response = client.post(
        "/auth/login",
        json={
            "email": "massi7@test.com",
            "password": "123456"
        }
    )

    return response.json()["access_token"]


def test_create_skill_requires_auth():
    response = client.post(
        "/skills/",
        json={
            "name": "Testing",
            "level": "Beginner",
            "category": "QA",
            "years_of_experience": 1
        }
    )

    assert response.status_code == 401

def test_create_skill_with_auth():
    token = get_auth_token()

    response = client.post(
        "/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "TestingSkill",
            "level": "Beginner",
            "category": "QA",
            "years_of_experience": 1
        }
    )

    assert response.status_code == 201

def test_assign_skill_forbidden():
    token = get_auth_token()

    response = client.post(
        "/skills/projects/1/skills/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [403, 404]    

def test_get_skills():
    response = client.get("/skills/")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert "items" in data
    assert isinstance(data["items"], list)