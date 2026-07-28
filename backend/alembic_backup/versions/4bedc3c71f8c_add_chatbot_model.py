"""add chatbot model

Revision ID: 4bedc3c71f8c
Revises: 8348f38fe30c
Create Date: 2026-07-18 10:37:05.437324
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4bedc3c71f8c"
down_revision: Union[str, Sequence[str], None] = "8348f38fe30c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "chatbots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("slug", sa.String(length=150), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "DRAFT",
                "TRAINING",
                "READY",
                "PAUSED",
                "ARCHIVED",
                name="chatbotstatus",
            ),
            nullable=False,
        ),
        sa.Column("avatar", sa.String(length=500), nullable=True),
        sa.Column("welcome_message", sa.Text(), nullable=True),
        sa.Column("placeholder_text", sa.String(length=255), nullable=True),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("public_uuid", sa.String(length=64), nullable=True),
        sa.Column("last_trained_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name=op.f("fk_chatbots_organization_id_organizations"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["created_by"],
            ["users.id"],
            name=op.f("fk_chatbots_created_by_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_chatbots")),
        sa.UniqueConstraint(
            "organization_id",
            "slug",
            name="uq_chatbot_org_slug",
        ),
        sa.UniqueConstraint(
            "public_uuid",
            name=op.f("uq_chatbots_public_uuid"),
        ),
    )

    op.create_index(
        "ix_chatbot_organization",
        "chatbots",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        "ix_chatbot_status",
        "chatbots",
        ["status"],
        unique=False,
    )

    op.create_index(
        "ix_chatbot_public_uuid",
        "chatbots",
        ["public_uuid"],
        unique=False,
    )

    # NOTE:
    # No index on "id" because the PRIMARY KEY already creates one.


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index("ix_chatbot_public_uuid", table_name="chatbots")
    op.drop_index("ix_chatbot_status", table_name="chatbots")
    op.drop_index("ix_chatbot_organization", table_name="chatbots")

    op.drop_table("chatbots")

    # Drop the PostgreSQL enum type after dropping the table.
    chatbot_status = sa.Enum(
        "DRAFT",
        "TRAINING",
        "READY",
        "PAUSED",
        "ARCHIVED",
        name="chatbotstatus",
    )
    chatbot_status.drop(op.get_bind(), checkfirst=True)