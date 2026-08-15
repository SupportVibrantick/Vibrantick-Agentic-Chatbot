import uuid

import pytest_asyncio


@pytest_asyncio.fixture
async def second_user(client):
    email = f"{uuid.uuid4()}@example.com"

    response = await client.post(
        "/api/auth/register",
        json={
            "full_name": "Second User",
            "email": email,
            "password": "Password123!",
        },
    )

    assert response.status_code == 201

    return response.json()