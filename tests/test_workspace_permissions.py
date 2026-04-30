


# owner can access to workspace 

def test_owner_can_access_workspace(client, token, test_workspace, test_membership):
    response = client.get(
        f"/workspaces/{test_workspace.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


# Member can't access to workspace 

def test_non_member_cannot_access_workspace(client, db, test_workspace):
    from app.models.user import User
    from app.core.security import hash_password

    other_user = User(
        email="other@test.com",
        full_name="Other User",
        hashed_password=hash_password("123456"),
        is_active=True,
        is_verified=True,
    )
    db.add(other_user)
    db.commit()
    db.refresh(other_user)

    # login
    response = client.post(
        "/auth/login",
        json={
            "email": other_user.email,
            "password": "123456"
        }
    )

    token = response.json()["access_token"]

    # tenta accesso
    response = client.get(
        f"/workspaces/{test_workspace.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


# Memeber can't delete workspace

def test_member_cannot_delete_workspace(client, db, test_workspace, test_user, token):
    from app.models.membership import Membership

    member = Membership(
        user_id=test_user.id,
        workspace_id=test_workspace.id,
        role="member"
    )
    db.add(member)
    db.commit()

    response = client.delete(
        f"/workspaces/{test_workspace.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [403, 401]