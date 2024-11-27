"""Add name to wallet

Revision ID: 007d93667be4
Revises: 63854b78c748
Create Date: 2024-11-27 18:06:37.198301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '007d93667be4'
down_revision: Union[str, None] = '63854b78c748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trade_pairs')
    op.drop_table('pair_price_snapshot')
    op.add_column('wallets', sa.Column('name', sa.String(length=100), nullable=False))
    op.create_unique_constraint(None, 'wallets', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'wallets', type_='unique')
    op.drop_column('wallets', 'name')
    op.create_table('pair_price_snapshot',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('symbol', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('current_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pair_price_snapshot_pkey'),
    sa.UniqueConstraint('symbol', name='pair_price_snapshot_symbol_key')
    )
    op.create_table('trade_pairs',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('ticker_buy', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('ticker_sell', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('average_buy_price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('available_quantity', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('first_trade_created_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('last_trade_updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('trades_updated_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='trade_pairs_pkey'),
    sa.UniqueConstraint('ticker_buy', 'ticker_sell', name='uix_ticker_buy_ticker_sell')
    )
    # ### end Alembic commands ###