from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


DatabaseSession = Annotated[Session, Depends(get_db)]


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