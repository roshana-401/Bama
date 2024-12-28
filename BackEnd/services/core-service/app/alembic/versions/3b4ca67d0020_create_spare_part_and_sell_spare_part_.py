"""create spare part and sell spare part table

Revision ID: 3b4ca67d0020
Revises: cc2bf5545a3d
Create Date: 2024-12-28 13:27:19.450843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql import text, func
# revision identifiers, used by Alembic.
revision: str = '3b4ca67d0020'
down_revision: Union[str, None] = 'cc2bf5545a3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.create_table(
        'spare_parts',
        sa.Column('spare_parts_id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text('gen_random_uuid()')),
        sa.Column('spare_parts_name', sa.String, nullable=False),
        sa.Column('model_id', UUID(as_uuid=True), sa.ForeignKey('model.model_id', ondelete="CASCADE"), nullable=False),
        sa.Column('price', sa.String, nullable=False),
        sa.Column('Operation', ENUM('new', 'used', name='operationstatus',create_type=False), nullable=False),
        sa.ForeignKeyConstraint(['model_id'], ['model.model_id'], ondelete="CASCADE"),  
    )

    op.create_table(
        'Sell_spare_parts',
        sa.Column('sell_spare_parts_id', UUID(as_uuid=True), primary_key=True, nullable=False, server_default=text('gen_random_uuid()')),
        sa.Column('phone_number', sa.String, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('spare_parts_id', UUID(as_uuid=True), sa.ForeignKey('spare_parts.spare_parts_id', ondelete="CASCADE"), nullable=False),
        sa.Column('date_create', sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('city_id', UUID(as_uuid=True), sa.ForeignKey('city.city_id', ondelete="CASCADE"), nullable=False),
        sa.Column('date_update', sa.TIMESTAMP(timezone=True), nullable=True, onupdate=func.now()),
        
        sa.ForeignKeyConstraint(['spare_parts_id'], ['spare_parts.spare_parts_id'], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(['city_id'], ['city.city_id'], ondelete="CASCADE")
    )


def downgrade() -> None:
    op.drop_table('Sell_spare_parts')
    op.drop_table('spare_parts')
