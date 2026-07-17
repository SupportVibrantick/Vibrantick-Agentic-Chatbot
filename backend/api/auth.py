from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from core.logging import get_logger
from database.unit_of_work import UnitOfWork
from dependencies.auth import get_current_user
from dependencies.database import get_uow
from models.user import User
from schemas.auth import Token, UserRegister, UserResponse
from services.auth_service import AuthService

logger = get_logger("admin")

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user_data: UserRegister,
    uow: UnitOfWork = Depends(get_uow),
):
    logger.info(f"Registration request received for {user_data.email}")

    auth_service = AuthService(uow)

    try:
        user = await auth_service.register(user_data)

        logger.info(f"User registered successfully: {user.email}")

        return user

    except ValueError as exc:
        logger.warning(
            f"Registration failed for {user_data.email}: {exc}"
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception(
            f"Unexpected error while registering {user_data.email}"
        )
        raise


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow: UnitOfWork = Depends(get_uow),
):
    logger.info(f"Login request: {form_data.username}")

    auth_service = AuthService(uow)

    token = await auth_service.login(
        form_data.username,
        form_data.password,
    )

    if token is None:
        logger.warning(
            f"Invalid login attempt: {form_data.username}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    logger.info(
        f"User logged in successfully: {form_data.username}"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_current_logged_in_user(
    current_user: User = Depends(get_current_user),
):
    logger.info(
        f"Current user profile requested: {current_user.email}"
    )

    return current_user