"""Add field message table in project_name

Revision ID: 107b864759a0
Revises: ee074aeba0fa
Create Date: 2024-08-12 14:47:51.802309

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "107b864759a0"
down_revision: Union[str, None] = "ee074aeba0fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("messages", sa.Column("project_name", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("messages", "project_name")
    # ### end Alembic commands ###
