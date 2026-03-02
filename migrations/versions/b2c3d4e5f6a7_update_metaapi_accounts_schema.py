"""update metaapi_accounts schema: drop api_token, add login/server/platform

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-02 14:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('metaapi_accounts', schema=None) as batch_op:
        batch_op.drop_column('api_token')
        batch_op.add_column(sa.Column('login', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('server', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('platform', sa.String(length=10), nullable=False, server_default='mt4'))


def downgrade():
    with op.batch_alter_table('metaapi_accounts', schema=None) as batch_op:
        batch_op.drop_column('platform')
        batch_op.drop_column('server')
        batch_op.drop_column('login')
        batch_op.add_column(sa.Column('api_token', sa.Text(), nullable=True))
