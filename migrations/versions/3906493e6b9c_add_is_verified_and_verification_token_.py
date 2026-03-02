"""add is_verified and verification_token to users

Revision ID: 3906493e6b9c
Revises: 0763d677d453
Create Date: 2026-02-18 18:19:25.994941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3906493e6b9c'
down_revision = '0763d677d453'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_verified and verification_token to existing users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_verified', sa.Boolean(), nullable=True, server_default='0'))
        batch_op.add_column(sa.Column('verification_token', sa.String(length=256), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('verification_token')
        batch_op.drop_column('is_verified')
