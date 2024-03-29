"""create posts table

Revision ID: 12617ba89931
Revises: 
Create Date: 2021-11-10 15:43:14.981879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12617ba89931'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('alembic_posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                                        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('alembic_posts')
    pass
