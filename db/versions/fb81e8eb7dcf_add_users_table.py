"""add users table

Revision ID: fb81e8eb7dcf
Revises: 8c068daa48d2
Create Date: 2024-10-03 22:04:49.367466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb81e8eb7dcf'
down_revision: Union[str, None] = '8c068daa48d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
     sa.Column("user_id", sa.Integer(), nullable=False, autoincrement=True),
     sa.Column("email", sa.String(), nullable=True),
     sa.Column("password", sa.String(), nullable=False),
     sa.Column("username", sa.String(), nullable=False),
     sa.Column("role", sa.String(), nullable=False),
     sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
     sa.PrimaryKeyConstraint("user_id", name="users_pkey"),
     sa.UniqueConstraint("email", name="users_email_unique")
     )
    pass    


def downgrade() -> None:
    # op.drop_table("users")
    pass

# op.create_table(..
# ..
# ) --> script is fine

# op.create_table
# (
# ...
# ) --> does not work