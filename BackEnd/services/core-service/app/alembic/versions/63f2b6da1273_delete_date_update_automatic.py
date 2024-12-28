"""delete date update automatic

Revision ID: 63f2b6da1273
Revises: 4cefe15c7a76
Create Date: 2024-12-28 14:43:34.242146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63f2b6da1273'
down_revision: Union[str, None] = '4cefe15c7a76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'Sell_car', 
        'date_update', 
        existing_type=sa.TIMESTAMP(timezone=True),
        nullable=True,
    )

def downgrade():
    op.alter_column(
        'Sell_car',
        'date_update',
        existing_type=sa.TIMESTAMP(timezone=True),
        nullable=True,
        server_default=sa.func.now(),
    )
