"""add content column to post table

Revision ID: 0b9cb73da3fe
Revises: 24bf21142644
Create Date: 2023-02-25 07:51:53.021138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b9cb73da3fe'
down_revision = '24bf21142644'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', "content")
    pass
