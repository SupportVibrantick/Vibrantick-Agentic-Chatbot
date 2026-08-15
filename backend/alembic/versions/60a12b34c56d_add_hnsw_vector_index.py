"""add HNSW vector index on document_chunks

Revision ID: 60a12b34c56d
Revises: 42c09d08f20d
Create Date: 2026-08-12 18:00:00.000000

"""
from typing import Sequence, Union
from alembic import op

revision: str = '60a12b34c56d'
down_revision: Union[str, Sequence[str], None] = '42c09d08f20d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_document_chunks_embedding_hnsw "
        "ON document_chunks USING hnsw (embedding vector_cosine_ops);"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_document_chunks_embedding_hnsw;")
