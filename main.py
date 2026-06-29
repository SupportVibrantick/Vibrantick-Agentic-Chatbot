import models


from fastapi import FastAPI
from sqlalchemy import text

from api.auth import router as auth_router
from database.base import Base
from database.engine import engine
from core.logger import logger
from core.settings import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(auth_router)


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