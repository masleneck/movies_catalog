"""Create movie table

Revision ID: f315842f5460
Revises:
Create Date: 2025-04-05 00:32:25.065563

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f315842f5460"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS citext;')
    op.create_table(
        "movies",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column(
            "title", postgresql.CITEXT(length=120), nullable=False
        ),
        sa.Column(
            "description",
            sa.Text(),
            server_default="",
            nullable=False,
        ),
        sa.Column("release_date", sa.Date(), nullable=True),
        sa.Column("duration", sa.SMALLINT(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_movies_title"), "movies", ["title"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_movies_title"), table_name="movies")
    op.drop_table("movies")
    # ### end Alembic commands ###
