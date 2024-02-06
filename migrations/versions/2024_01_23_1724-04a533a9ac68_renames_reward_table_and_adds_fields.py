"""renames reward_table and adds fields

Revision ID: 04a533a9ac68
Revises: 2f4a4f2c7a8d
Create Date: 2024-01-23 17:24:02.764411-08:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '04a533a9ac68'
down_revision = '2f4a4f2c7a8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rule',
    sa.Column('uuid', sa.String(length=56), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('rule_name', sa.String(length=255), nullable=False),
    sa.Column('rule_type', sa.String(length=56), nullable=False),
    sa.Column('trigger_field', sa.String(length=56), nullable=False),
    sa.Column('timing_type', sa.String(length=56), nullable=False),
    sa.Column('days_prior', sa.Integer(), nullable=True),
    sa.Column('sending_time', sa.String(length=56), nullable=False),
    sa.Column('timezone', sa.String(length=56), nullable=False),
    sa.Column('manager_id', sa.Integer(), nullable=False),
    sa.Column('sending_managers_account_id', sa.Integer(), nullable=False),
    sa.Column('sending_managers_program_id', sa.Integer(), nullable=False),
    sa.Column('bucket_customization_id', sa.Integer(), nullable=False),
    sa.Column('bucket_customization_price', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('memo', sa.String(length=255), nullable=False),
    sa.Column('recipient_note', sa.String(length=255), nullable=False),
    sa.Column('company_values', sa.JSON(), nullable=False),
    sa.Column('segmented_by', sa.JSON(), nullable=True),
    sa.Column('anniversary_years', sa.JSON(), nullable=True),
    sa.Column('onboarding_period', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.Integer(), nullable=False),
    sa.Column('time_updated', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_rule_company_id'), 'rule', ['company_id'], unique=False)
    op.create_index(op.f('ix_rule_manager_id'), 'rule', ['manager_id'], unique=False)
    op.create_index(op.f('ix_rule_rule_name'), 'rule', ['rule_name'], unique=False)
    op.create_index(op.f('ix_rule_rule_type'), 'rule', ['rule_type'], unique=False)
    op.create_index(op.f('ix_rule_sending_managers_program_id'), 'rule', ['sending_managers_program_id'], unique=False)
    op.create_index(op.f('ix_rule_sending_time'), 'rule', ['sending_time'], unique=False)
    op.create_index(op.f('ix_rule_timing_type'), 'rule', ['timing_type'], unique=False)
    op.create_index(op.f('ix_rule_trigger_field'), 'rule', ['trigger_field'], unique=False)
    op.create_index(op.f('ix_rule_uuid'), 'rule', ['uuid'], unique=False)
    op.drop_index('ix_reward_company_id', table_name='reward')
    op.drop_index('ix_reward_uuid', table_name='reward')
    op.drop_table('reward')
    op.add_column('staged_reward', sa.Column('bucket_customization_id', sa.Integer(), nullable=False))
    op.add_column('staged_reward', sa.Column('bucket_customization_price', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reward',
    sa.Column('uuid', sa.String(length=56), nullable=False),
    sa.Column('company_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('rule', sa.Text(), nullable=False),
    sa.Column('users', sa.Text(), nullable=False),
    sa.Column('reward_info', sa.Text(), nullable=False),
    sa.Column('time_created', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('time_updated', sa.Integer(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index('ix_reward_uuid', 'reward', ['uuid'], unique=False)
    op.create_index('ix_reward_company_id', 'reward', ['company_id'], unique=False)
    op.drop_index(op.f('ix_rule_uuid'), table_name='rule')
    op.drop_index(op.f('ix_rule_trigger_field'), table_name='rule')
    op.drop_index(op.f('ix_rule_timing_type'), table_name='rule')
    op.drop_index(op.f('ix_rule_sending_time'), table_name='rule')
    op.drop_index(op.f('ix_rule_sending_managers_program_id'), table_name='rule')
    op.drop_index(op.f('ix_rule_rule_type'), table_name='rule')
    op.drop_index(op.f('ix_rule_rule_name'), table_name='rule')
    op.drop_index(op.f('ix_rule_manager_id'), table_name='rule')
    op.drop_index(op.f('ix_rule_company_id'), table_name='rule')
    op.drop_index(op.f('ix_rule_cadence_type'), table_name='rule')
    op.drop_index(op.f('ix_rule_cadence'), table_name='rule')
    op.drop_table('rule')
    op.drop_column('staged_reward', 'bucket_customization_id')
    op.drop_column('staged_reward', 'bucket_customization_price')

    # ### end Alembic commands ###