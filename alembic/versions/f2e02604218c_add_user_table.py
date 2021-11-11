"""add user table

Revision ID: f2e02604218c
Revises: 9b7e40d6e118
Create Date: 2021-11-10 20:43:20.511908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2e02604218c'
down_revision = '9b7e40d6e118'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('alembic_users',
                            sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('email', sa.String(), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')) 
    pass


def downgrade():
    op.drop_table('alembic_users')
    pass
