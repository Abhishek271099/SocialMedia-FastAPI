"""add foreign-key to posts table

Revision ID: bfd956bab06b
Revises: d630c5a9f2e9
Create Date: 2023-12-29 15:35:36.809904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfd956bab06b'
down_revision: Union[str, None] = 'd630c5a9f2e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
