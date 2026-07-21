from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base
from backend.enums import TaskPriority
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    String,
    Text,
    func,
)

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(
            TaskPriority,
            name="task_priority",
            native_enum=False,
            create_constraint=True,
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        default=TaskPriority.MEDIUM,
        server_default=TaskPriority.MEDIUM.value,
        nullable=False,
    )
    
    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )