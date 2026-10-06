from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings


# --------------------------------------------------
# PASSWORD HASHING
# --------------------------------------------------

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Convert a plain password into a secure Argon2 hash.
    """
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain password against its stored Argon2 hash.
    """
    return password_hash.verify(
        password,
        hashed_password,
    )


# --------------------------------------------------
# JWT CONFIGURATION
# --------------------------------------------------

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# --------------------------------------------------
# CREATE ACCESS TOKEN
# --------------------------------------------------

def create_access_token(user_id: int) -> str:
    """
    Create a JWT access token for an authenticated user.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.AUTH_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return token


# --------------------------------------------------
# DECODE ACCESS TOKEN
# --------------------------------------------------

def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    Raises:
        jwt.InvalidTokenError:
            If the token is invalid or expired.
    """

    payload = jwt.decode(
        token,
        settings.AUTH_SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    return payload