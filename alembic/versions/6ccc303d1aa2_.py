"""empty message

Revision ID: 6ccc303d1aa2
Revises: manual_revision, 8b7dff36ca91
Create Date: 2026-06-25 14:14:22.063043

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ccc303d1aa2'
down_revision: Union[str, None] = ('manual_revision', '8b7dff36ca91')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
