"""change user id and link user id to bigint

Revision ID: 7f3455ca2285
Revises:
Create Date: 2026-09-02 21:08:11.207232
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7f3455ca2285"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "link_user_id_fkey",
        "link",
        type_="foreignkey",
    )

    op.alter_column(
        "user",
        "user_id",
        existing_type=sa.VARCHAR(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        postgresql_using="user_id::bigint",
    )

    op.alter_column(
        "link",
        "user_id",
        existing_type=sa.VARCHAR(),
        type_=sa.BigInteger(),
        existing_nullable=True,
        postgresql_using="user_id::bigint",
    )

    op.create_foreign_key(
        "link_user_id_fkey",
        "link",
        "user",
        ["user_id"],
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "link_user_id_fkey",
        "link",
        type_="foreignkey",
    )

    op.alter_column(
        "link",
        "user_id",
        existing_type=sa.BigInteger(),
        type_=sa.VARCHAR(),
        existing_nullable=True,
        postgresql_using="user_id::varchar",
    )

    op.alter_column(
        "user",
        "user_id",
        existing_type=sa.BigInteger(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="user_id::varchar",
    )

    op.create_foreign_key(
        "link_user_id_fkey",
        "link",
        "user",
        ["user_id"],
        ["user_id"],
    )