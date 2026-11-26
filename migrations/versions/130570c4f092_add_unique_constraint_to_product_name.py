"""Add unique constraint to product name

Revision ID: 130570c4f092
Revises: 53edba92d042
Create Date: 2026-11-14 22:02:01.299037

"""

from typing import Sequence, Union

from alembic import op

revision: str = "130570c4f092"
down_revision: Union[str, Sequence[str], None] = "53edba92d042"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_products_name", "products", ["name"])


def downgrade() -> None:
    op.drop_constraint("uq_products_name", "products", type_="unique")
