from sqlalchemy import select
from sqlalchemy.orm import Session

from backend import models, schemas


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session) -> list[models.Task]:
    statement = select(models.Task).order_by(models.Task.id)

    return list(db.scalars(statement).all())


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)