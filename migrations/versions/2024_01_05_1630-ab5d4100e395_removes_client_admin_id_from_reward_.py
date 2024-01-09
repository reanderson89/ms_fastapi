"""removes client_admin_id from reward table

Revision ID: ab5d4100e395
Revises: 0e34f44d229c
Create Date: 2024-01-05 16:30:26.671750-08:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ab5d4100e395'
down_revision = '0e34f44d229c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_reward_client_admin_id', table_name='reward')
    op.drop_column('reward', 'client_admin_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reward', sa.Column('client_admin_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_index('ix_reward_client_admin_id', 'reward', ['client_admin_id'], unique=False)
    # ### end Alembic commands ###
