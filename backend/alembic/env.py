from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy import create_engine, pool

# ---------------------------------------------------------
# Determine application environment
# ---------------------------------------------------------
# Priority:
# 1. Explicit APP_ENV environment variable
# 2. Alembic -x environment=... argument
# 3. development
#
# Example:
#   $env:APP_ENV="testing"
#   uv run alembic current
#
# Or:
#   uv run alembic -x environment=testing current
# ---------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

x_args = context.get_x_argument(as_dictionary=True)

environment = (
    os.getenv("APP_ENV")
    or x_args.get("environment")
    or "development"
)

# Make APP_ENV visible before importing settings/config.
os.environ["APP_ENV"] = environment

from core.settings import settings
from database.base import Base

# Import all models so they are registered with Base.metadata
import models  # noqa: F401


# ---------------------------------------------------------
# Database URL
# ---------------------------------------------------------

database_url = settings.DATABASE_URL.replace(
    "postgresql+asyncpg://",
    "postgresql+psycopg://",
)

config.set_main_option(
    "sqlalchemy.url",
    database_url,
)

print("=" * 80)
print("ALEMBIC ENVIRONMENT:", environment)
print("ALEMBIC DATABASE URL:", database_url)
print("=" * 80)


target_metadata = Base.metadata


# ---------------------------------------------------------
# Offline migrations
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Online migrations
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Execute
# ---------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()