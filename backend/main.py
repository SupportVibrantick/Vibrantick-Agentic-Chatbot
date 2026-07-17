import models   
from fastapi import FastAPI
from sqlalchemy import text
from api.organizations import router as organizations_router
from api.public_invitations import router as public_invitations_router
from api import invitations
from api.auth import router as auth_router
from api.users import router as users_router
from database.base import Base
from database.engine import engine
    
from api.test_email import router as test_email_router
from api import organization_members
from core.settings import settings
from core.logging import get_logger

logger = get_logger("system")
    


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(auth_router)

app.include_router(test_email_router)

app.include_router(
    public_invitations_router,
    prefix="/api",
)
app.include_router(
    invitations.router,
    prefix="/api",
)

app.include_router(
    users_router,
    prefix="/api/users",
    tags=["Users"],
)

app.include_router(
    organizations_router,
    prefix="/api",
)


app.include_router(
    organization_members.router,
    prefix="/api",
)



@app.on_event("startup")
async def startup():

    logger.info(f"{settings.APP_NAME} started")

    try:

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))

        logger.success("Database connected successfully")

    except Exception as e:
        logger.error(f"Database connection failed: {e}")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Vibrantic AI"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

print("MAIN.PY FINISHED LOADING")
