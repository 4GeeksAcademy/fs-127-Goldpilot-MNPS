"""allow multiple wallets per user: drop unique constraint on user_id

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-03-02 16:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade():
    # SQLite does not support DROP CONSTRAINT; recreate the table without the
    # UniqueConstraint on user_id by using the rename-copy-drop pattern.
    op.execute("ALTER TABLE metaapi_accounts RENAME TO _metaapi_accounts_old")
    op.create_table(
        'metaapi_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),   # no UniqueConstraint
        sa.Column('account_id', sa.String(length=255), nullable=False),
        sa.Column('login', sa.String(length=64), nullable=True),
        sa.Column('server', sa.String(length=120), nullable=True),
        sa.Column('platform', sa.String(length=10), nullable=False, server_default='mt4'),
        sa.Column('broker_name', sa.String(length=120), nullable=True),
        sa.Column('account_type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.execute(
        "INSERT INTO metaapi_accounts "
        "SELECT id, user_id, account_id, login, server, platform, "
        "broker_name, account_type, status, created_at "
        "FROM _metaapi_accounts_old"
    )
    op.execute("DROP TABLE _metaapi_accounts_old")


def downgrade():
    # Restore unique constraint on user_id
    op.execute("ALTER TABLE metaapi_accounts RENAME TO _metaapi_accounts_old")
    op.create_table(
        'metaapi_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.String(length=255), nullable=False),
        sa.Column('login', sa.String(length=64), nullable=True),
        sa.Column('server', sa.String(length=120), nullable=True),
        sa.Column('platform', sa.String(length=10), nullable=False, server_default='mt4'),
        sa.Column('broker_name', sa.String(length=120), nullable=True),
        sa.Column('account_type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )
    op.execute(
        "INSERT INTO metaapi_accounts "
        "SELECT id, user_id, account_id, login, server, platform, "
        "broker_name, account_type, status, created_at "
        "FROM _metaapi_accounts_old"
    )
    op.execute("DROP TABLE _metaapi_accounts_old")
