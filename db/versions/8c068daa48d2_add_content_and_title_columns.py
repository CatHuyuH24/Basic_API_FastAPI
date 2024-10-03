"""add content and title columns

Revision ID: 8c068daa48d2
Revises: 706decfc11b6
Create Date: 2024-10-03 21:57:01.011964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c068daa48d2'
down_revision: Union[str, None] = '706decfc11b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("title", sa.String(), nullable=True, server_default=""))
    op.add_column("posts",sa.Column("content", sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column("posts","title")
    op.drop_column("posts","content")
    pass
