"""add foreign-key to alembic_posts table

Revision ID: 04f1abad19b3
Revises: f2e02604218c
Create Date: 2021-11-10 20:54:21.740897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04f1abad19b3'
down_revision = 'f2e02604218c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('alembic_posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="alembic_posts", referent_table="alembic_users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="alembic_posts")
    op.drop_column('alembic_posts', 'owner_id') 
    pass
