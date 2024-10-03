"""user-id to owner-id

Revision ID: beb7fb23fd33
Revises: fb81e8eb7dcf
Create Date: 2024-10-03 23:28:36.410330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'beb7fb23fd33'
down_revision: Union[str, None] = 'fb81e8eb7dcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("posts","user_id",new_column_name="owner_id", existing_type=sa.Integer, existing_nullable=False)
    pass


def downgrade() -> None:
    op.alter_column("posts","owner_id",new_column_name="user_id", existing_type=sa.Integer(), existing_nullable=False)
    pass
