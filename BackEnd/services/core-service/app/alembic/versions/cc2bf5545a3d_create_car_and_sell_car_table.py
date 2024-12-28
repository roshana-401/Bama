"""create car and sell car table

Revision ID: cc2bf5545a3d
Revises: 12f4d6226078
Create Date: 2024-12-28 13:10:35.312446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ENUM
from App.domain.models.operation_status import OperationStatus

# revision identifiers, used by Alembic.
revision: str = 'cc2bf5545a3d'
down_revision: Union[str, None] = '12f4d6226078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE TYPE operationstatus AS ENUM ('used', 'new');
    """)
    op.create_table(
        'car',
        sa.Column('car_id', UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column('car_name', sa.String(), nullable=False),
        sa.Column('model_id', UUID(as_uuid=True), nullable=False),
        sa.Column('price', sa.String(), nullable=False),
        sa.Column('color', sa.String(), nullable=False),
        sa.Column('gearbox', sa.String(), nullable=False),
        sa.Column('KM', sa.String(), nullable=False),
        sa.Column('Operation', sa.Enum(OperationStatus,name="operationstatus"), nullable=False),
        sa.Column('year', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['model_id'], ['model.model_id'], ondelete="CASCADE"),
    )

    op.create_table(
        'Sell_car',
        sa.Column('sell_car_id', UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('car_id', UUID(as_uuid=True), nullable=False),
        sa.Column('date_create', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('city_id', UUID(as_uuid=True), nullable=False),
        sa.Column('date_update', sa.TIMESTAMP(timezone=True), nullable=True, onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(['car_id'], ['car.car_id'], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(['city_id'], ['city.city_id'], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table('Sell_car')
    op.drop_table('car')
    op.execute("DROP TYPE operationstatus;")
