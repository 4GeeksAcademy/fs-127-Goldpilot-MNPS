"""add region to metaapi_accounts

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-03-02 17:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('metaapi_accounts', sa.Column('region', sa.String(length=30), nullable=True))


def downgrade():
    with op.batch_alter_table('metaapi_accounts', schema=None) as batch_op:
        batch_op.drop_column('region')
