"""empty message

Revision ID: e58f029c12b7
Revises: 21c8f95dfd90
Create Date: 2024-11-14 11:03:17.594244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e58f029c12b7'
down_revision: Union[str, None] = '21c8f95dfd90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', 'password', existing_type=sa.String(), nullable=True)
    op.alter_column('users', 'role_id', existing_type=sa.Integer(), nullable=True)


def downgrade() -> None:
    op.alter_column('users', 'password', existing_type=sa.String(), nullable=False)
    op.alter_column('users', 'role_id', existing_type=sa.Integer(), nullable=False)
