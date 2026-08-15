import pytest_asyncio


@pytest_asyncio.fixture
async def chatbot(
    authenticated_client,
    organization,
):
    response = await authenticated_client.post(
        f"/chatbots/organizations/{organization['id']}",
        json={
            "name": "Test Chatbot",
            "description": "Chatbot for testing",
            "welcome_message": "Hello!",
            "placeholder_text": "Ask me anything...",
            "is_public": False,
        },
    )

    assert response.status_code == 201

    return response.json()