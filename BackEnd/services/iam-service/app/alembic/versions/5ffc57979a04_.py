"""empty message

Revision ID: 5ffc57979a04
Revises: e58f029c12b7
Create Date: 2024-11-14 20:05:03.477278

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ffc57979a04'
down_revision: Union[str, None] = 'e58f029c12b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute('ALTER TABLE users ALTER COLUMN user_id SET DEFAULT gen_random_uuid();')

def downgrade():
    op.execute('ALTER TABLE users ALTER COLUMN user_id SET DEFAULT uuid_generate_v4();')
