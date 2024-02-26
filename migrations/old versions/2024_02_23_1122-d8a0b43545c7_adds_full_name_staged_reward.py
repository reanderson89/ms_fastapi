"""adds full_name staged_reward

Revision ID: d8a0b43545c7
Revises: 5e6bdde58ce4
Create Date: 2024-02-23 11:22:55.592174-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8a0b43545c7'
down_revision = '5e6bdde58ce4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staged_reward', sa.Column('full_name', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_staged_reward_full_name'), 'staged_reward', ['full_name'], unique=False)
    op.execute("""
        UPDATE staged_reward
        SET full_name = first_name || ' ' || last_name
    """)
    op.alter_column('staged_reward', 'full_name', existing_type=sa.String(length=255), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_staged_reward_full_name'), table_name='staged_reward')
    op.drop_column('staged_reward', 'full_name')
    # ### end Alembic commands ###
