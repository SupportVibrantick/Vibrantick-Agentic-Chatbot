async def test_create_organization_success(
    authenticated_client,
):
    response = await authenticated_client.post(
        "/api/organizations",
        json={
            "name": "OpenAI",
            "description": "AI Company",
            "logo": None,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "OpenAI"
    assert data["description"] == "AI Company"


async def test_update_organization_success(
    authenticated_client,
    organization,
):
    response = await authenticated_client.put(
        f"/api/organizations/{organization['id']}",
        json={
            "name": "Updated Organization",
            "description": "Updated Description",
            "logo": None,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Organization"
    assert data["description"] == "Updated Description"


async def test_delete_organization_success(
    authenticated_client,
    organization,
):
    response = await authenticated_client.delete(
        f"/api/organizations/{organization['id']}"
    )

    assert response.status_code == 204