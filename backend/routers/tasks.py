from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import get_db


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


DatabaseSession = Annotated[Session, Depends(get_db)]
TaskId = Annotated[int, Path(ge=1)]


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


@router.get(
    "",
    response_model=list[schemas.TaskResponse],
)
def read_tasks(db: DatabaseSession) -> list[models.Task]:
    return crud.get_tasks(db=db)


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
)
def read_task(
    task_id: TaskId,
    db: DatabaseSession,
) -> models.Task:
    db_task = crud.get_task(db=db, task_id=task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return db_task