"""empty message

Revision ID: fe4161855630
Revises: 
Create Date: 2024-11-13 18:52:51.002557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision: str = 'fe4161855630'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'role',
        sa.Column('role_id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
        sa.Column('role_name', sa.String(), nullable=False)
    )
    op.create_table(
        'users',
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, default=uuid.uuid4, primary_key=True),
        sa.Column('phone_number', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('date_register', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('date_update_Profile', sa.TIMESTAMP(timezone=True), nullable=True, default=None, onupdate=sa.func.now()),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.role_id'), nullable=False),
    )
    
def downgrade():
    op.drop_table('users')
    op.drop_table('role')