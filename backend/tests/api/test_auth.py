import uuid


async def test_register_user(client):
    email = f"{uuid.uuid4()}@example.com"

    response = await client.post(
        "/api/auth/register",
        json={
            "full_name": "Test User",
            "email": email,
            "password": "Password123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "Test User"
    assert data["email"] == email
    assert "id" in data
    
async def test_register_duplicate_email(client):
    email = f"{uuid.uuid4()}@example.com"

    payload = {
        "full_name": "Test User",
        "email": email,
        "password": "Password123!",
    }

    await client.post(
        "/api/auth/register",
        json=payload,
    )

    response = await client.post(
        "/api/auth/register",
        json=payload,
    )

    assert response.status_code == 400
    
async def test_login(client):
    email = f"{uuid.uuid4()}@example.com"

    await client.post(
        "/api/auth/register",
        json={
            "full_name": "Test User",
            "email": email,
            "password": "Password123!",
        },
    )

    response = await client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    token = response.json()

    assert "access_token" in token
    assert token["token_type"] == "bearer"
    
async def test_login_invalid_password(client):
    response = await client.post(
        "/api/auth/login",
        data={
            "username": "abc@test.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401