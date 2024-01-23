"""create current vacancy table

Revision ID: f92bc35ab301
Revises: 373ab027675a
Create Date: 2024-01-23 20:04:09.983058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f92bc35ab301'
down_revision: Union[str, None] = '373ab027675a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('current_vacancy',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('value', sa.String(length=10), nullable=False),
    sa.Column('vacancy_name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('current_vacancy')
    # ### end Alembic commands ###
