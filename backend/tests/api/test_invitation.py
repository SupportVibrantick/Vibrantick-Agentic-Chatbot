async def test_create_invitation_success(
    authenticated_client,
    organization,
):
    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/invitations",
        json={
            "email": "invite@example.com",
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "invite@example.com"
    assert data["role"] == "MEMBER"


async def test_list_invitations_success(
    authenticated_client,
    organization,
):
    create = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/invitations",
        json={
            "email": "invite@example.com",
            "role": "MEMBER",
        },
    )

    assert create.status_code == 201

    response = await authenticated_client.get(
        f"/api/organizations/{organization['id']}/invitations"
    )

    assert response.status_code == 200

    data = response.json()

    assert "invitations" in data
    assert len(data["invitations"]) == 1

    invitation = data["invitations"][0]

    assert invitation["email"] == "invite@example.com"
    assert invitation["role"] == "MEMBER"


async def test_cancel_invitation_success(
    authenticated_client,
    organization,
):
    create = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/invitations",
        json={
            "email": "invite@example.com",
            "role": "MEMBER",
        },
    )

    assert create.status_code == 201

    invitation = create.json()

    response = await authenticated_client.delete(
        f"/api/organizations/{organization['id']}/invitations/{invitation['id']}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == invitation["id"]
    assert data["status"] == "CANCELLED"