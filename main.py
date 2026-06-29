
from fastapi import FastAPI
from logger import logger
from settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


@app.on_event("startup")
async def startup():

    logger.info(f"{settings.APP_NAME} started")


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