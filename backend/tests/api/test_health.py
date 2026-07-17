async def test_docs_page(client):
    response = await client.get("/docs")

    assert response.status_code == 200