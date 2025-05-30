"""Updating Election Columns

Revision ID: 8fd90767b330
Revises: 619c25c376cc
Create Date: 2025-04-06 12:59:51.813853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fd90767b330'
down_revision: Union[str, None] = '619c25c376cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('election', sa.Column('polling_date', sa.Date(), nullable=False))
    op.add_column('election', sa.Column('seat_count', sa.Integer(), nullable=False))
    op.drop_column('election', 'election_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('election', sa.Column('election_date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_column('election', 'seat_count')
    op.drop_column('election', 'polling_date')
    # ### end Alembic commands ###
