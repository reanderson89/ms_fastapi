"""“initial”

Revision ID: cf9f4708d1e9
Revises: 
Create Date: 2023-04-20 15:07:37.904432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf9f4708d1e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # hello-world example for future use?
    # op.create_table(
    #     'bar',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String(50), nullable=False),
    #     sa.Column('description', sa.Unicode(200)),
    # )
    # op.create_table(
    #     'foo',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String(50), nullable=False),
    #     sa.Column('description', sa.Unicode(200)),
    # )
    pass


def downgrade() -> None:
    pass
