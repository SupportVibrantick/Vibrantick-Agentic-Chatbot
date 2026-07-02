import models


from fastapi import FastAPI
from sqlalchemy import text
from api.organizations import router as organizations_router

from api import invitations
from api.auth import router as auth_router
from api.users import router as users_router
from database.base import Base
from database.engine import engine
from core.logger import logger
from api import organization_members
from core.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(auth_router)

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

    Base.metadata.create_all(bind=engine)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
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
    
