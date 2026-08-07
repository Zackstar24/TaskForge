"""add task ownership

Revision ID: 58a5350ade53
Revises: 4f0299d2050a
Create Date: 2026-08-07 15:45:39.669652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58a5350ade53'
down_revision: Union[str, Sequence[str], None] = '4f0299d2050a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NAMING_CONVENTION = {
    "fk": (
        "fk_%(table_name)s_"
        "%(column_0_name)s_"
        "%(referred_table_name)s"
    ),
}


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table(
        "tasks",
        schema=None,
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.create_index(
            batch_op.f("ix_tasks_user_id"),
            ["user_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            "fk_tasks_user_id_users",
            "users",
            ["user_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table(
        "tasks",
        schema=None,
        naming_convention=NAMING_CONVENTION,
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_tasks_user_id_users",
            type_="foreignkey",
        )
        batch_op.drop_index(
            batch_op.f("ix_tasks_user_id"),
        )
        batch_op.drop_column("user_id")
    # ### end Alembic commands ###
