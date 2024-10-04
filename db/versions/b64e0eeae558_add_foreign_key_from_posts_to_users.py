"""add foreign key from posts to users

Revision ID: b64e0eeae558
Revises: beb7fb23fd33
Create Date: 2024-10-03 23:49:15.435117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b64e0eeae558'
down_revision: Union[str, None] = 'beb7fb23fd33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key("fk_posts_users",source_table="posts",
                           referent_table="users", local_cols=["owner_id"],
                             remote_cols=["user_id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint(constraint_name="fk_posts_users", table_name="posts", type_="foreignkey")
    pass
