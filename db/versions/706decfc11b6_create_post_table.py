"""create post table

Revision ID: 706decfc11b6
Revises: 
Create Date: 2024-10-01 22:45:18.685725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
# if only 2 lines:
# INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
# INFO  [alembic.runtime.migration] Will assume transactional DDL. (without the 'Running upgrade' line)
# ==> alembic not working -> solved by deleting the 'alembic_version' table in the database and then redoing the migration
revision: str = '706decfc11b6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# op means operation; sa means sqlalchemy; the first is the table's name, subsequent are the columns

def upgrade() -> None: #handle the new changes - adding more
    op.create_table(
        "posts", 
        sa.Column("post_id",sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column("user_id",sa.Integer(), nullable=False))
    pass


def downgrade() -> None: #handle removing some
    op.drop_table("posts") # the name of the table
    pass
