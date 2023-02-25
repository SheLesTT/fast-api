"""empty message

Revision ID: 6e0222ae1b2a
Revises: 4486766ee3b4
Create Date: 2023-02-25 08:08:39.412638

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6e0222ae1b2a'
down_revision = '4486766ee3b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table="users",
                          local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')

    pass
