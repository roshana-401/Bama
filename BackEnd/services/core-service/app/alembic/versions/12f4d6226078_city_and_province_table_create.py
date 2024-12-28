"""city and province table create

Revision ID: 12f4d6226078
Revises: 525d17e21e86
Create Date: 2024-12-28 02:30:06.010547

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '12f4d6226078'
down_revision: Union[str, None] = '525d17e21e86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'province',
        sa.Column('province_id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()")),
        sa.Column('province_name', sa.String(), nullable=False, unique=True)
    )
    op.create_table(
        'city',
        sa.Column('city_id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()")),
        sa.Column('city_name', sa.String(), nullable=False),
        sa.Column('province_id', UUID(as_uuid=True), sa.ForeignKey('province.province_id', ondelete="CASCADE"), nullable=False)
    )



def downgrade() -> None:
    op.drop_table('city')
    op.drop_table('province')
