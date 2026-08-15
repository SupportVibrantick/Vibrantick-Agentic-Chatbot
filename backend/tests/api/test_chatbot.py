import uuid


CHATBOT_PAYLOAD = {
    "name": "Test Chatbot",
    "description": "Chatbot for testing",
    "avatar": None,
    "welcome_message": "Hello!",
    "placeholder_text": "Ask me anything...",
    "is_public": False,
}


async def _create_chatbot(
    authenticated_client,
    organization_id: int,
):
    return await authenticated_client.post(
        f"/chatbots/organizations/{organization_id}",
        json=CHATBOT_PAYLOAD,
    )


async def _register_user(client):
    email = f"{uuid.uuid4()}@example.com"
    password = "Password123!"

    response = await client.post(
        "/api/auth/register",
        json={
            "full_name": "Chatbot Test User",
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201

    return {
        "email": email,
        "password": password,
        "user": response.json(),
    }


async def _login(client, email: str, password: str):
    response = await client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )


async def test_create_chatbot_requires_authentication(
    client,
    organization,
):
    response = await client.post(
        f"/chatbots/organizations/{organization['id']}",
        json=CHATBOT_PAYLOAD,
    )

    assert response.status_code == 401


async def test_owner_can_create_chatbot(
    authenticated_client,
    organization,
):
    response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert response.status_code == 201

    data = response.json()

    assert data["organization_id"] == organization["id"]
    assert data["name"] == CHATBOT_PAYLOAD["name"]

    # The organization owner is the authenticated creator.
    assert data["created_by"] == organization["owner_id"]


async def test_member_cannot_create_chatbot(
    authenticated_client,
    client,
    organization,
):
    # Register a second user.
    second_user = await _register_user(client)

    # Current authenticated user is the organization owner.
    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    # Authenticate as the member.
    await _login(
        client,
        second_user["email"],
        second_user["password"],
    )

    response = await client.post(
        f"/chatbots/organizations/{organization['id']}",
        json={
            **CHATBOT_PAYLOAD,
            "name": "Member Chatbot",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


async def test_member_can_list_chatbots(
    authenticated_client,
    client,
    organization,
):
    # Owner creates a chatbot first.
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    # Register second user.
    second_user = await _register_user(client)

    # Owner adds second user as MEMBER.
    member_response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert member_response.status_code == 201

    # Login as MEMBER.
    await _login(
        client,
        second_user["email"],
        second_user["password"],
    )

    response = await client.get(
        f"/chatbots/organizations/{organization['id']}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["organization_id"] == organization["id"]


async def test_non_member_cannot_list_chatbots(
    authenticated_client,
    client,
    organization,
):
    # Create chatbot in the organization.
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    # Register another user but DON'T add them to the organization.
    outsider = await _register_user(client)

    await _login(
        client,
        outsider["email"],
        outsider["password"],
    )

    response = await client.get(
        f"/chatbots/organizations/{organization['id']}",
    )

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "You are not a member of this organization"
    )


async def test_non_member_cannot_get_chatbot(
    authenticated_client,
    client,
    organization,
):
    # Owner creates chatbot.
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    chatbot = create_response.json()

    # Register outsider.
    outsider = await _register_user(client)

    await _login(
        client,
        outsider["email"],
        outsider["password"],
    )

    response = await client.get(
        f"/chatbots/{chatbot['id']}",
    )

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "You are not a member of this organization"
    )


async def test_member_can_get_chatbot(
    authenticated_client,
    client,
    organization,
):
    # Owner creates chatbot.
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    chatbot = create_response.json()

    # Register second user.
    second_user = await _register_user(client)

    # Owner adds member.
    member_response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert member_response.status_code == 201

    # Login as member.
    await _login(
        client,
        second_user["email"],
        second_user["password"],
    )

    response = await client.get(
        f"/chatbots/{chatbot['id']}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == chatbot["id"]
    assert data["organization_id"] == organization["id"]


async def test_get_missing_chatbot_returns_404(
    authenticated_client,
):
    response = await authenticated_client.get(
        "/chatbots/999999999",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Chatbot not found."