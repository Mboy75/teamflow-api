
import pytest


def test_create_skill_with_auth(client, token):
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


def test_create_skill_requires_auth(client):
    response = client.post(
        "/skills/",
        json={
            "name": "NoAuthSkill",
            "level": "Beginner",
            "category": "QA",
            "years_of_experience": 1
        }
    )

    assert response.status_code == 401


def test_assign_skill_success(client, token, test_project):
    # crea skill
    create_response = client.post(
        "/skills/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Python",
            "level": "Advanced",
            "category": "Backend",
            "years_of_experience": 3
        }
    )

    skill_id = create_response.json()["id"]

    # assegna skill al project
    response = client.post(
        f"/skills/projects/{test_project.id}/skills/{skill_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_assign_skill_forbidden(client, token):
    response = client.post(
        "/skills/projects/999/skills/1",
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