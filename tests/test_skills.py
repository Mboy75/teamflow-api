from fastapi.testclient import TestClient
from app.main import app
import pytest


def get_auth_token(client):
    response = client.post(
        "/auth/login",
        data={   # ✅ usa data
            "username": "massi7@test.com",  # username, non email
            "password": "123456"
        }
    )

    print("LOGIN:", response.status_code, response.json())  # debug temporaneo

    return response.json()["access_token"]


def test_create_skill_requires_auth(client):
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

@pytest.mark.skip(reason="Needs test user in test database")
def test_create_skill_with_auth(client):
    token = get_auth_token(client)

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

@pytest.mark.skip(reason="Needs test user in test database")
def test_assign_skill_forbidden(client):
    token = get_auth_token(client)

    response = client.post(
        "/skills/projects/1/skills/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [403, 404]    

def test_get_skills(client):
    response = client.get("/skills/")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "skip" in data
    assert "limit" in data
    assert "items" in data
    assert isinstance(data["items"], list)