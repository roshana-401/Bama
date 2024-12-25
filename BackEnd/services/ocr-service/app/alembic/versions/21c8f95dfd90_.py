"""empty message

Revision ID: 21c8f95dfd90
Revises: fe4161855630
Create Date: 2024-11-13 21:14:28.267632

"""
from enum import Enum
from App.domain.models.user_status import UserStatus
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21c8f95dfd90'
down_revision: Union[str, None] = 'fe4161855630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TYPE userstatus AS ENUM ('unverified', 'verified', 'active', 'inactive');
    """)
    op.add_column('users', sa.Column('status', sa.Enum(UserStatus, name='userstatus'), nullable=False, server_default='unverified'))


def downgrade() -> None:
    op.drop_column('users', 'status')
    op.execute("DROP TYPE userstatus;")