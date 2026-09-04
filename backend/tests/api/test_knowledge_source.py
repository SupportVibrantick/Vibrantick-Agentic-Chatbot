import pytest
from sqlalchemy import select

from models.document import Document, DocumentStatus
from models.document_chunk import DocumentChunk
from models.knowledge_source import (
    KnowledgeSource,
    KnowledgeSourceStatus,
)


@pytest.mark.asyncio
async def test_upload_text_source_creates_document_and_chunks(
    authenticated_client,
    chatbot,
    db_session,
):
    # ---------------------------------------------------------
    # 1. Create knowledge base
    # ---------------------------------------------------------
    response = await authenticated_client.post(
        f"/knowledge-bases/chatbots/{chatbot['id']}",
        json={
            "name": "Ingestion Test KB",
            "description": "Knowledge base for ingestion testing",
            "embedding_provider": "bge",
            "embedding_model": "BAAI/bge-m3",
            "chunk_size": 1000,
            "chunk_overlap": 200,
        },
    )

    assert response.status_code == 201, response.text

    knowledge_base = response.json()

    # ---------------------------------------------------------
    # 2. Upload text document
    # ---------------------------------------------------------
    content = (
        b"Vibrantick is building an agentic AI SaaS platform. "
        b"The platform supports knowledge bases, retrieval, "
        b"conversations, and AI agents."
    )

    response = await authenticated_client.post(
        f"/api/knowledge-bases/{knowledge_base['id']}/sources/upload",
        files={
            "file": (
                "test.txt",
                content,
                "text/plain",
            )
        },
    )

    assert response.status_code == 201, response.text

    source = response.json()

    assert source["name"] == "test.txt"
    assert source["status"] == "ready"

    source_id = source["id"]

    # ---------------------------------------------------------
    # 3. Verify KnowledgeSource
    # ---------------------------------------------------------
    source_result = await db_session.get(
        KnowledgeSource,
        source_id,
    )

    assert source_result is not None
    assert (
        source_result.knowledge_base_id
        == knowledge_base["id"]
    )
    assert (
        source_result.status
        == KnowledgeSourceStatus.READY
    )

    # ---------------------------------------------------------
    # 4. Verify Document
    # ---------------------------------------------------------
    result = await db_session.execute(
        select(Document).where(
            Document.knowledge_base_id
            == knowledge_base["id"]
        )
    )

    documents = list(result.scalars().all())

    assert len(documents) == 1

    document = documents[0]

    assert document.knowledge_base_id == knowledge_base["id"]
    assert document.original_filename == "test.txt"
    assert document.status == DocumentStatus.READY

    # ---------------------------------------------------------
    # 5. Verify DocumentChunks
    # ---------------------------------------------------------
    result = await db_session.execute(
        select(DocumentChunk).where(
            DocumentChunk.document_id == document.id
        )
    )

    chunks = list(result.scalars().all())

    assert len(chunks) > 0

    # ---------------------------------------------------------
    # 6. Critical architecture assertion
    # ---------------------------------------------------------
    for chunk in chunks:
        assert chunk.document_id == document.id
        assert chunk.document_id != source_id

    # ---------------------------------------------------------
    # 7. Verify embeddings
    # ---------------------------------------------------------
    for chunk in chunks:
        assert chunk.embedding is not None
        assert len(chunk.embedding) == 1024