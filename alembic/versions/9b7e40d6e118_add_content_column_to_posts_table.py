"""add content column to posts table

Revision ID: 9b7e40d6e118
Revises: 12617ba89931
Create Date: 2021-11-10 19:30:33.078588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b7e40d6e118'
down_revision = '12617ba89931'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('alembic_posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('alembic_posts', 'content')
    pass
