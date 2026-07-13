from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post(
    "",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate,
    db: DatabaseSession,
) -> models.Task:
    return crud.create_task(db=db, task=task)