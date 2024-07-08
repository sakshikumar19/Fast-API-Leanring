"""create posts table

Revision ID: 3a9d9d455906
Revises: 
Create Date: 2024-07-09 00:12:41.151010

"""

# run > python -m alembic upgrade 3a9d9d455906 > upgrade number is the revision ID for the script you want


from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a9d9d455906'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
        )
    pass


def downgrade() -> None:
    op.drop_table('posts') # needed command in case user wants to rollback changes
    pass
