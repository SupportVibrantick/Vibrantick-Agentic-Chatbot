import pytest_asyncio


@pytest_asyncio.fixture
async def organization(
    authenticated_client,
):
    response = await authenticated_client.post(
        "/api/organizations",
        json={
            "name": "Test Organization",
            "description": "Organization for testing",
            "logo": None,
        },
    )

    assert response.status_code == 201

    return response.json()