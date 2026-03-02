"""add metaapi_accounts table

Revision ID: a1b2c3d4e5f6
Revises: 6550a060bd32
Create Date: 2026-03-02 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '6550a060bd32'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('metaapi_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.String(length=255), nullable=False),
        sa.Column('api_token', sa.Text(), nullable=False),
        sa.Column('broker_name', sa.String(length=120), nullable=True),
        sa.Column('account_type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )


def downgrade():
    op.drop_table('metaapi_accounts')
