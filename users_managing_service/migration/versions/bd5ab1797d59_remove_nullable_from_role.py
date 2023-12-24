"""remove nullable from role

Revision ID: bd5ab1797d59
Revises: 4ba5bc2ef03b
Create Date: 2023-12-23 18:48:04.258270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bd5ab1797d59'
down_revision: Union[str, None] = '4ba5bc2ef03b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=mysql.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=mysql.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###