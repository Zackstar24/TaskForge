import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Return a secure hash for a plain-text password."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Check a plain-text password against a stored hash."""
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def get_secret_key() -> str:
    secret_key = os.getenv("TASKFORGE_SECRET_KEY")

    if not secret_key:
        raise RuntimeError(
            "TASKFORGE_SECRET_KEY environment variable is not set",
        )

    return secret_key


def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        get_secret_key(),
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> int:
    payload = jwt.decode(
        token,
        get_secret_key(),
        algorithms=[ALGORITHM],
    )

    subject = payload.get("sub")

    if subject is None:
        raise jwt.InvalidTokenError(
            "Token subject is missing",
        )

    try:
        return int(subject)
    except ValueError as error:
        raise jwt.InvalidTokenError(
            "Token subject is invalid",
        ) from error