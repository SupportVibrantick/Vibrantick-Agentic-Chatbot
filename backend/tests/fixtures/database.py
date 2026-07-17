import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import AsyncSessionLocal, engine
from database.session import get_db
from main import app
from tests.utils.alembic import alembic_manager


@pytest_asyncio.fixture(
    scope="session",
    autouse=True,
)
async def migrate_database():
    """
    Apply all Alembic migrations once before the test session
    and dispose the SQLAlchemy engine afterwards.
    """

    alembic_manager.upgrade()

    yield

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(
    migrate_database,
) -> AsyncSession:
    """
    Provide a clean AsyncSession for each test and override
    FastAPI's get_db dependency.
    """

    async with AsyncSessionLocal() as session:

        async def override_get_db():
            yield session

        app.dependency_overrides[get_db] = override_get_db

        try:
            yield session

        finally:
            app.dependency_overrides.pop(
                get_db,
                None,
            )

            await session.rollback()
            await session.close()