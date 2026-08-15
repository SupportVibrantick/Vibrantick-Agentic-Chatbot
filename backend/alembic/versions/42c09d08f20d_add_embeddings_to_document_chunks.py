"""add embeddings to document chunks

Revision ID: 42c09d08f20d
Revises: 597a3aa30a58
Create Date: 2026-08-07 19:28:44.994114

"""
from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = '42c09d08f20d'
down_revision: Union[str, Sequence[str], None] = '597a3aa30a58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """
    No-op migration.

    The initial schema migration already creates the
    documents and document_chunks tables with a
    1024-dimensional embedding column.
    """
    pass


def downgrade() -> None:
    """
    No-op migration.

    The schema objects are owned by the initial migration.
    """
    pass