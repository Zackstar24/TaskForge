from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.enums import TaskPriority

class TaskBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )
    description: str | None = None
    completed: bool | None = None

    @model_validator(mode="after")
    def validate_update(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")

        if "title" in self.model_fields_set and self.title is None:
            raise ValueError("Title cannot be null")

        if "completed" in self.model_fields_set and self.completed is None:
            raise ValueError("Completed cannot be null")

        if "priority" in self.model_fields_set and self.priority is None:
            raise ValueError("Priority cannot be null")

        return self
    priority: TaskPriority | None = None
    
class TaskResponse(TaskBase):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )

    id: int
    completed: bool
    created_at: datetime