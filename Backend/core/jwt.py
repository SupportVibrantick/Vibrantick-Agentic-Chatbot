from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from core.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

JWTClaims = dict[str, Any]


def create_access_token(data: JWTClaims) -> str:
    """
    Create a JWT access token.
    """
    to_encode: JWTClaims = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode["exp"] = expire

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> JWTClaims | None:
    """
    Decode and validate a JWT token.
    """
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        return None