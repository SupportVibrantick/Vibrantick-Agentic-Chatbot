from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from core.settings import settings
from database.base import Base

# Import all models so they are registered with Base.metadata
import models  # noqa: F401

import sqlalchemy as sa

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Convert async URL to sync URL for Alembic
database_url = settings.DATABASE_URL.replace(
    "postgresql+asyncpg://",
    "postgresql+psycopg://",
)

config.set_main_option("sqlalchemy.url", database_url)
print("=" * 80)
print("ALEMBIC DATABASE URL:", database_url)
print("=" * 80)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()