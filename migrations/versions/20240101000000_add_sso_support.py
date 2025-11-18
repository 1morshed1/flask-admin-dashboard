"""Add SSO support to users

Revision ID: add_sso_support
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_sso_support'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Make password_hash nullable for SSO users
    op.alter_column('users', 'password_hash',
                    existing_type=sa.String(length=255),
                    nullable=True)
    
    # Add is_sso_user column
    op.add_column('users', sa.Column('is_sso_user', sa.Boolean(), 
                                      nullable=False, server_default='false'))


def downgrade():
    # Remove is_sso_user column
    op.drop_column('users', 'is_sso_user')
    
    # Make password_hash non-nullable again
    op.alter_column('users', 'password_hash',
                    existing_type=sa.String(length=255),
                    nullable=False)

