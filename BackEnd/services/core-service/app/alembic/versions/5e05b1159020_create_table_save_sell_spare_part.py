"""create table save sell spare part

Revision ID: 5e05b1159020
Revises: 79125d76acbf
Create Date: 2024-12-29 10:54:28.415803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e05b1159020'
down_revision: Union[str, None] = '79125d76acbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'saveSparePart',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('sell_spare_parts_id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'sell_spare_parts_id')
    )

def downgrade():
    op.drop_table('saveSparePart')
