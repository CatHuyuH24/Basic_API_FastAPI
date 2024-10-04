"""add created_at and published to posts

Revision ID: bf2156222019
Revises: b64e0eeae558
Create Date: 2024-10-04 15:01:06.562125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf2156222019'
down_revision: Union[str, None] = 'b64e0eeae558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), server_default='TRUE', nullable=False))
    op.add_column("posts",sa.Column("created_at", sa.TIMESTAMP(timezone=True),server_default=sa.text('NOW()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
