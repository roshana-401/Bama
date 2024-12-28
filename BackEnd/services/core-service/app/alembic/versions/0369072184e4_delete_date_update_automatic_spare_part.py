"""delete date update automatic spare part

Revision ID: 0369072184e4
Revises: 63f2b6da1273
Create Date: 2024-12-28 14:46:04.077269

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0369072184e4'
down_revision: Union[str, None] = '63f2b6da1273'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'Sell_spare_parts', 
        'date_update', 
        existing_type=sa.TIMESTAMP(timezone=True),
        nullable=True,
    )

def downgrade():
    op.alter_column(
        'Sell_spare_parts',
        'date_update',
        existing_type=sa.TIMESTAMP(timezone=True),
        nullable=True,
        server_default=sa.func.now(),
    )
