"""create trades table

Revision ID: d4b8bd73f2aa
Revises: d4e5f6a7b8c9
Create Date: 2026-03-04 21:06:25.401104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4b8bd73f2aa'
down_revision = 'd4e5f6a7b8c9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('trades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('wallet_id', sa.Integer(), nullable=True),
    sa.Column('meta_trade_id', sa.String(length=64), nullable=True),
    sa.Column('symbol', sa.String(length=20), nullable=False),
    sa.Column('trade_type', sa.String(length=10), nullable=False),
    sa.Column('lot_size', sa.Float(), nullable=True),
    sa.Column('open_price', sa.Float(), nullable=True),
    sa.Column('close_price', sa.Float(), nullable=True),
    sa.Column('stop_loss', sa.Float(), nullable=True),
    sa.Column('take_profit', sa.Float(), nullable=True),
    sa.Column('profit_loss', sa.Float(), nullable=False),
    sa.Column('opened_at', sa.DateTime(), nullable=False),
    sa.Column('closed_at', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['wallet_id'], ['metaapi_accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('trades')

