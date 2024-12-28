"""edited column gearbox

Revision ID: 4cefe15c7a76
Revises: 3b4ca67d0020
Create Date: 2024-12-28 13:43:03.973886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from App.domain.models.gearboxStatus import gearboxStatus
from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic.
revision: str = '4cefe15c7a76'
down_revision: Union[str, None] = '3b4ca67d0020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE TYPE gearboxstatus AS ENUM ('manual', 'automatic')")
    
    op.alter_column(
        'car',  
        'gearbox',     
        type_=postgresql.ENUM('manual', 'automatic', name='gearboxstatus'),
        existing_type=sa.String, 
        nullable=False, 
        postgresql_using="gearbox::gearboxstatus"
    )


def downgrade() -> None:
    op.alter_column(
        'your_table',
        'gearbox',
        type_=sa.String,  
        existing_type=postgresql.ENUM('manual', 'automatic', name='gearboxstatus'),
        nullable=False
    )
    op.execute("DROP TYPE gearboxstatus")