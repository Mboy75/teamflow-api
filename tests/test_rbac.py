def test_member_cannot_delete_workspace(client, token, test_workspace):
    response = client.delete(
        f"/workspaces/{test_workspace.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403