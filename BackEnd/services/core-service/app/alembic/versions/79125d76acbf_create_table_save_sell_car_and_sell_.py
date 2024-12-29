"""create table save sell car and sell spare part

Revision ID: 79125d76acbf
Revises: 0369072184e4
Create Date: 2024-12-29 10:50:56.268624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79125d76acbf'
down_revision: Union[str, None] = '0369072184e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'saveCar',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('sell_car_id', sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'sell_car_id')
    )

def downgrade():
    op.drop_table('saveCar')
