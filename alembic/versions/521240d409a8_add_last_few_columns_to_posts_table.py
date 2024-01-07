"""add last few columns to posts table

Revision ID: 521240d409a8
Revises: bfd956bab06b
Create Date: 2023-12-29 15:41:21.770939

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '521240d409a8'
down_revision: Union[str, None] = 'bfd956bab06b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column(
        "published", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column(
        "created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
