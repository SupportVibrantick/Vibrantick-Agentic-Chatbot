import uuid


KB_PAYLOAD = {
    "name": "Test Knowledge Base",
    "description": "Knowledge base for testing",
    "embedding_provider": "bge",
    "embedding_model": "BAAI/bge-m3",
    "chunk_size": 1000,
    "chunk_overlap": 200,
}


async def register_user(client):
    email = f"{uuid.uuid4()}@example.com"
    password = "Password123!"

    response = await client.post(
        "/api/auth/register",
        json={
            "full_name": "Knowledge Base Test User",
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


async def login(client, user):
    response = await client.post(
        "/api/auth/login",
        data={
            "username": user["email"],
            "password": user["password"],
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )


async def create_kb(
    authenticated_client,
    chatbot_id,
):
    return await authenticated_client.post(
        f"/knowledge-bases/chatbots/{chatbot_id}",
        json=KB_PAYLOAD,
    )


# ==========================================================
# CREATE
# ==========================================================


async def test_create_knowledge_base_requires_authentication(
    client,
    chatbot,
):
    response = await client.post(
        f"/knowledge-bases/chatbots/{chatbot['id']}",
        json=KB_PAYLOAD,
    )

    assert response.status_code == 401


async def test_owner_can_create_knowledge_base(
    authenticated_client,
    chatbot,
):
    response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert response.status_code == 201

    data = response.json()

    assert data["chatbot_id"] == chatbot["id"]
    assert data["name"] == KB_PAYLOAD["name"]
    assert data["embedding_provider"] == "bge"
    assert data["embedding_model"] == "BAAI/bge-m3"


async def test_member_cannot_create_knowledge_base(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    member = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": member["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    await login(client, member)

    response = await client.post(
        f"/knowledge-bases/chatbots/{chatbot['id']}",
        json=KB_PAYLOAD,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


# ==========================================================
# LIST
# ==========================================================


async def test_member_can_list_knowledge_bases(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    member = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": member["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    await login(client, member)

    response = await client.get(
        f"/knowledge-bases/chatbots/{chatbot['id']}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert data["items"][0]["chatbot_id"] == chatbot["id"]


async def test_outsider_cannot_list_knowledge_bases(
    authenticated_client,
    client,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    outsider = await register_user(client)

    await login(client, outsider)

    response = await client.get(
        f"/knowledge-bases/chatbots/{chatbot['id']}",
    )

    assert response.status_code == 403

    assert (
        response.json()["detail"]
        == "You are not a member of this organization"
    )


# ==========================================================
# GET
# ==========================================================


async def test_member_can_get_knowledge_base(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    knowledge_base = create_response.json()

    member = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": member["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    await login(client, member)

    response = await client.get(
        f"/knowledge-bases/{knowledge_base['id']}",
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == knowledge_base["id"]
    assert data["chatbot_id"] == chatbot["id"]


async def test_outsider_cannot_get_knowledge_base(
    authenticated_client,
    client,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    knowledge_base = create_response.json()

    outsider = await register_user(client)

    await login(client, outsider)

    response = await client.get(
        f"/knowledge-bases/{knowledge_base['id']}",
    )

    assert response.status_code == 403

    assert (
        response.json()["detail"]
        == "You are not a member of this organization"
    )


# ==========================================================
# UPDATE
# ==========================================================


async def test_member_cannot_update_knowledge_base(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    knowledge_base = create_response.json()

    member = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": member["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    await login(client, member)

    response = await client.patch(
        f"/knowledge-bases/{knowledge_base['id']}",
        json={
            "name": "Unauthorized Update",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


async def test_admin_can_update_knowledge_base(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    knowledge_base = create_response.json()

    admin = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": admin["email"],
            "role": "ADMIN",
        },
    )

    assert response.status_code == 201

    await login(client, admin)

    response = await client.patch(
        f"/knowledge-bases/{knowledge_base['id']}",
        json={
            "name": "Updated Knowledge Base",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Knowledge Base"


# ==========================================================
# DELETE
# ==========================================================


async def test_member_cannot_delete_knowledge_base(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    knowledge_base = create_response.json()

    member = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": member["email"],
            "role": "MEMBER",
        },
    )

    assert response.status_code == 201

    await login(client, member)

    response = await client.delete(
        f"/knowledge-bases/{knowledge_base['id']}",
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required"


async def test_admin_can_delete_knowledge_base(
    authenticated_client,
    client,
    organization,
    chatbot,
):
    create_response = await create_kb(
        authenticated_client,
        chatbot["id"],
    )

    assert create_response.status_code == 201

    knowledge_base = create_response.json()

    admin = await register_user(client)

    response = await authenticated_client.post(
        f"/api/organizations/{organization['id']}/members",
        json={
            "email": admin["email"],
            "role": "ADMIN",
        },
    )

    assert response.status_code == 201

    await login(client, admin)

    response = await client.delete(
        f"/knowledge-bases/{knowledge_base['id']}",
    )

    assert response.status_code == 204