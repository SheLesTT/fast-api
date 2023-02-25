"""add user table

Revision ID: 4486766ee3b4
Revises: 0b9cb73da3fe
Create Date: 2023-02-25 07:58:20.975782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4486766ee3b4'
down_revision = '0b9cb73da3fe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column("id", sa.Integer, nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_ar", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_column('users')
    pass
