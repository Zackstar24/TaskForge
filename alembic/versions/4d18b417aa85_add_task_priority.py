"""add task priority

Revision ID: 4d18b417aa85
Revises: 6d2cb7dbf02c
Create Date: 2026-07-20 19:25:46.360872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d18b417aa85'
down_revision: Union[str, Sequence[str], None] = '6d2cb7dbf02c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "priority",
                sa.Enum(
                    "low",
                    "medium",
                    "high",
                    name="task_priority",
                    native_enum=False,
                    create_constraint=False,
                ),
                server_default="medium",
                nullable=False,
            )
        )
        batch_op.create_check_constraint(
            "task_priority",
            "priority IN ('low', 'medium', 'high')",
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.drop_constraint(
            "task_priority",
            type_="check",
        )
        batch_op.drop_column("priority")
