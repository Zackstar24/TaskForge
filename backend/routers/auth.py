from typing import Annotated

import jwt
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import get_db
from backend.security import (
    create_access_token,
    decode_access_token,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


bearer_scheme = HTTPBearer(
    auto_error=False,
)


DatabaseSession = Annotated[
    Session,
    Depends(get_db),
]

BearerCredentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]


def unauthorized_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )


def get_current_user(
    credentials: BearerCredentials,
    db: DatabaseSession,
) -> models.User:
    if credentials is None:
        raise unauthorized_exception()

    try:
        user_id = decode_access_token(
            credentials.credentials,
        )
    except jwt.InvalidTokenError as error:
        raise unauthorized_exception() from error

    db_user = crud.get_user(
        db=db,
        user_id=user_id,
    )

    if db_user is None:
        raise unauthorized_exception()

    return db_user


CurrentUser = Annotated[
    models.User,
    Depends(get_current_user),
]


@router.post(
    "/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: schemas.UserCreate,
    db: DatabaseSession,
) -> models.User:
    try:
        return crud.create_user(
            db=db,
            user=user,
        )
    except IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        ) from error


@router.post(
    "/login",
    response_model=schemas.TokenResponse,
)
def login_user(
    credentials: schemas.UserLogin,
    db: DatabaseSession,
) -> schemas.TokenResponse:
    db_user = crud.get_user_by_email(
        db=db,
        email=credentials.email,
    )

    if (
        db_user is None
        or not verify_password(
            credentials.password,
            db_user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    access_token = create_access_token(
        db_user.id,
    )

    return schemas.TokenResponse(
        access_token=access_token,
    )


@router.get(
    "/me",
    response_model=schemas.UserResponse,
)
def read_current_user(
    current_user: CurrentUser,
) -> models.User:
    return current_user