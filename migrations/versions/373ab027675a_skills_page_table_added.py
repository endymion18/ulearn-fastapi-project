"""skills page table added

Revision ID: 373ab027675a
Revises: 36059817c75b
Create Date: 2024-01-23 00:16:53.990849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '373ab027675a'
down_revision: Union[str, None] = '36059817c75b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skills_page',
    sa.Column('id', sa.Integer(), sa.Identity(always=False), nullable=False),
    sa.Column('value', sa.String(length=10), nullable=False),
    sa.Column('table_data', postgresql.JSON(astext_type=sa.Text()), nullable=True),
    sa.Column('img_path', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skills_page')
    # ### end Alembic commands ###
