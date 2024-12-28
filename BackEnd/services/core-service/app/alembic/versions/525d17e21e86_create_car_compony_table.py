"""create car compony table

Revision ID: 525d17e21e86
Revises: 
Create Date: 2024-12-27 18:10:48.946597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text
# revision identifiers, used by Alembic.
revision: str = '525d17e21e86'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'car_compony',
        sa.Column('car_compony_id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()")),
        sa.Column('car_compony_name', sa.String(), nullable=False, unique=True)
    )

    op.create_table(
        'model',
        sa.Column('model_id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text("gen_random_uuid()")),
        sa.Column('model_name', sa.String(), nullable=False, unique=True),
        sa.Column('car_compony_id', UUID(as_uuid=True), sa.ForeignKey('car_compony.car_compony_id', ondelete="CASCADE"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('model')
    op.drop_table('car_compony')
