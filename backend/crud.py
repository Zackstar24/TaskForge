from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.security import hash_password


def create_task(
    db: Session,
    task: schemas.TaskCreate,
) -> models.Task:
    db_task = models.Task(**task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session) -> list[models.Task]:
    statement = select(models.Task).order_by(models.Task.id)

    return list(db.scalars(statement).all())


def get_task(
    db: Session,
    task_id: int,
) -> models.Task | None:
    return db.get(models.Task, task_id)


def update_task(
    db: Session,
    db_task: models.Task,
    task: schemas.TaskUpdate,
) -> models.Task:
    update_data = task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task


def delete_task(
    db: Session,
    db_task: models.Task,
) -> None:
    db.delete(db_task)
    db.commit()

def get_user(
    db: Session,
    user_id: int,
) -> models.User | None:
    return db.get(models.User, user_id)

def get_user_by_email(
    db: Session,
    email: str,
) -> models.User | None:
    statement = select(models.User).where(
        models.User.email == email,
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    user: schemas.UserCreate,
) -> models.User:
    db_user = models.User(
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_user)

    return db_user