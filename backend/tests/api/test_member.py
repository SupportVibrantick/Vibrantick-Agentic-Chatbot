async def test_add_member_success(
    authenticated_client,
    organization,
    second_user,
):
    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["organization_id"] == organization["id"]
    assert data["user_id"] == second_user["id"]
    assert data["role"] == "MEMBER"