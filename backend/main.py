from contextlib import asynccontextmanager

import models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from api import invitations
from api import organization_members
from api.auth import router as auth_router
from api.chat import router as chat_router
from api.chatbot_ai_configs import (
    router as chatbot_ai_configs_router,
)
from api.documents import (
    router as documents_router,
)
from api.knowledge_bases import (
    router as knowledge_bases_router,
)
from api.organizations import (
    router as organizations_router,
)
from api.public_invitations import (
    router as public_invitations_router,
)
from api.test_email import (
    router as test_email_router,
)
from api.users import (router as users_router,)
from api.chatbot import router as chatbot_router
from api.conversations import router as conversations_router
from api.knowledge_sources import router as knowledge_sources_router
from core.logging import get_logger
from core.settings import settings
from database.engine import engine

logger = get_logger("system")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        f"Starting {settings.APP_NAME} v{settings.APP_VERSION}",
    )

    try:
        async with engine.connect() as connection:
            await connection.execute(
                text("SELECT 1"),
            )

        logger.success(
            "Database connected successfully.",
        )

    except Exception as exc:
        logger.exception(
            f"Database connection failed: {exc}",
        )

    yield

    logger.info(
        "Shutting down application.",
    )

    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# -----------------------------------------------------
# CORS
# -----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------
# Authentication
# -----------------------------------------------------

app.include_router(
    auth_router,
)

# -----------------------------------------------------
# Test Utilities
# -----------------------------------------------------

app.include_router(
    test_email_router,
)

# -----------------------------------------------------
# Public APIs
# -----------------------------------------------------

app.include_router(
    public_invitations_router,
    prefix="/api",
)

# -----------------------------------------------------
# Protected APIs
# -----------------------------------------------------

app.include_router(
    invitations.router,
    prefix="/api",
)

app.include_router(
    organizations_router,
    prefix="/api",
)

app.include_router(
    organization_members.router,
    prefix="/api",
)

app.include_router(
    users_router,
    prefix="/api/users",
)

app.include_router(
    knowledge_bases_router,
)

app.include_router(
    chatbot_ai_configs_router,
)

app.include_router(
    documents_router,
    prefix="/api",
)

app.include_router(
    chat_router,
    prefix="/api",
)
#-----------------------------------------------------
# Chatbot & Conversation APIs  
#-----------------------------------------------------
app.include_router(chatbot_router)
app.include_router(conversations_router, prefix="/api")
app.include_router(knowledge_sources_router, prefix="/api")
# -----------------------------------------------------
# Health
# -----------------------------------------------------

@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "database": "connected",
    }


print("MAIN.PY FINISHED LOADING")