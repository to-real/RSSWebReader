"""add source_type to feeds

Revision ID: 9e2f6f4a1a2b
Revises: 15627a69fc6d
Create Date: 2026-02-27 19:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e2f6f4a1a2b"
down_revision: Union[str, Sequence[str], None] = "15627a69fc6d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("feeds", sa.Column("source_type", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("feeds", "source_type")
