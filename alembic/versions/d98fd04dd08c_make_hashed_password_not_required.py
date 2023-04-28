"""make hashed password not required

Revision ID: d98fd04dd08c
Revises: d48d7f7d6777
Create Date: 2023-04-27 22:28:20.367660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd98fd04dd08c'
down_revision = 'd48d7f7d6777'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
