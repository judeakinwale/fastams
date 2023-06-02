"""update: update settings with business hours details

Revision ID: 2d783705c4d6
Revises: 34c5b20c5e6d
Create Date: 2023-05-22 20:28:58.983729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d783705c4d6'
down_revision = '34c5b20c5e6d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('settings', sa.Column('opens', sa.String(), nullable=True))
    op.add_column('settings', sa.Column('closes', sa.String(), nullable=True))
    op.add_column('settings', sa.Column('open_days', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('settings', 'open_days')
    op.drop_column('settings', 'closes')
    op.drop_column('settings', 'opens')
    # ### end Alembic commands ###