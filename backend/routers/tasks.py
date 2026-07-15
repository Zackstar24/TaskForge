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


def get_task_or_404(
    db: Session,
    task_id: int,
) -> models.Task:
    db_task = crud.get_task(db=db, task_id=task_id)

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return db_task


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
    return get_task_or_404(db=db, task_id=task_id)


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse,
)
def update_task(
    task_id: TaskId,
    task: schemas.TaskUpdate,
    db: DatabaseSession,
) -> models.Task:
    db_task = get_task_or_404(db=db, task_id=task_id)

    return crud.update_task(
        db=db,
        db_task=db_task,
        task=task,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_task(
    task_id: TaskId,
    db: DatabaseSession,
) -> None:
    db_task = get_task_or_404(db=db, task_id=task_id)

    crud.delete_task(
        db=db,
        db_task=db_task,
    )