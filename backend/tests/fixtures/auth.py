import uuid

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app


@pytest_asyncio.fixture
async def registered_user(client):
    email = f"{uuid.uuid4()}@example.com"
    password = "Password123!"

    response = await client.post(
        "/api/auth/register",
        json={
            "full_name": "Test User",
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


@pytest_asyncio.fixture
async def authenticated_client(
    client,
    registered_user,
):
    auth_client = AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    )

    try:
        response = await auth_client.post(
            "/api/auth/login",
            data={
                "username": registered_user["email"],
                "password": registered_user["password"],
            },
        )

        assert response.status_code == 200

        token = response.json()["access_token"]

        auth_client.headers.update(
            {"Authorization": f"Bearer {token}"}
        )

        yield auth_client

    finally:
        await auth_client.aclose()