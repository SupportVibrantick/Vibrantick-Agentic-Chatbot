import uuid

import pytest

from services.llm.provider_factory import ProviderFactory


CHATBOT_PAYLOAD = {
    "name": "Test Chatbot",
    "description": "Chatbot for testing",
    "avatar": None,
    "welcome_message": "Hello!",
    "placeholder_text": "Ask me anything...",
    "is_public": False,
}


class FakeLLMProvider:
    async def chat(self, request):
        return "Test assistant response"

    async def stream(self, request):
        yield "Test "
        yield "assistant response"


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


async def _login(
    client,
    email: str,
    password: str,
):
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


# ==========================================================
# Existing chatbot tests
# ==========================================================


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

    assert data["created_by"] == organization["owner_id"]


async def test_member_cannot_create_chatbot(
    authenticated_client,
    client,
    organization,
):
    second_user = await _register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

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
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    second_user = await _register_user(client)

    member_response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert member_response.status_code == 201

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
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

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
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    chatbot = create_response.json()

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
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201

    chatbot = create_response.json()

    second_user = await _register_user(client)

    member_response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": second_user["email"],
            "role": "MEMBER",
        },
    )

    assert member_response.status_code == 201

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


# ==========================================================
# Conversation security tests
# ==========================================================


@pytest.mark.asyncio
async def test_cannot_reuse_conversation_with_different_chatbot(
    authenticated_client,
    organization,
    monkeypatch,
):
    monkeypatch.setattr(
        ProviderFactory,
        "create",
        lambda: FakeLLMProvider(),
    )

    # Create chatbot A.
    response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert response.status_code == 201
    chatbot_a = response.json()

    # Create chatbot B in the same organization.
    response = await authenticated_client.post(
        f"/chatbots/organizations/{organization['id']}",
        json={
            **CHATBOT_PAYLOAD,
            "name": "Second Chatbot",
        },
    )

    assert response.status_code == 201
    chatbot_b = response.json()

    # Create a conversation using chatbot A.
    response = await authenticated_client.post(
        "/api/chat",
        json={
            "chatbot_id": chatbot_a["id"],
            "message": "Hello chatbot A",
        },
    )

    assert response.status_code == 200

    conversation_id = response.json()["conversation_id"]

    # Attempt to reuse chatbot A's conversation with chatbot B.
    response = await authenticated_client.post(
        "/api/chat",
        json={
            "chatbot_id": chatbot_b["id"],
            "conversation_id": conversation_id,
            "message": "This must not be allowed",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Conversation does not belong to this chatbot."
    )


@pytest.mark.asyncio
async def test_non_member_cannot_chat_with_private_chatbot(
    authenticated_client,
    client,
    organization,
    monkeypatch,
):
    monkeypatch.setattr(
        ProviderFactory,
        "create",
        lambda: FakeLLMProvider(),
    )

    # Owner creates a private chatbot.
    create_response = await _create_chatbot(
        authenticated_client,
        organization["id"],
    )

    assert create_response.status_code == 201
    chatbot = create_response.json()

    # Register an outsider.
    outsider = await _register_user(client)

    await _login(
        client,
        outsider["email"],
        outsider["password"],
    )

    response = await client.post(
        "/api/chat",
        json={
            "chatbot_id": chatbot["id"],
            "message": "I should not have access",
        },
    )

    assert response.status_code == 403
    assert (
        response.json()["detail"]
        == "You are not a member of this organization"
    )


async def test_stream_requires_authentication(
    client,
    organization,
):
    response = await client.post(
        "/api/chat/stream",
        json={
            "chatbot_id": 1,
            "message": "Unauthenticated request",
        },
    )

    assert response.status_code == 401