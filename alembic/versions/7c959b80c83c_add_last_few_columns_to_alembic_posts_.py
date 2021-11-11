"""add last few columns to alembic_posts table

Revision ID: 7c959b80c83c
Revises: 04f1abad19b3
Create Date: 2021-11-10 21:30:51.292909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c959b80c83c'
down_revision = '04f1abad19b3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('alembic_posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('alembic_posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))) 
    pass


def downgrade():
    op.drop_column('alembic_posts', 'published')
    op.drop_column('alembic_posts', 'created_at') 
    pass
