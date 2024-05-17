"""modify portofolio

Revision ID: b14325be6ef5
Revises: 776669b56453
Create Date: 2024-05-11 20:38:14.385271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b14325be6ef5'
down_revision: Union[str, None] = '776669b56453'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
