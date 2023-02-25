"""add few new columns

Revision ID: 2fcf23e5b6fc
Revises: 6e0222ae1b2a
Create Date: 2023-02-25 08:18:51.436845

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2fcf23e5b6fc'
down_revision = '6e0222ae1b2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable=False,
                                          server_default=sa.text('now()')))

    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
