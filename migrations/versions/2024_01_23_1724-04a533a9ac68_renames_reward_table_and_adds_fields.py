"""renames reward_table and adds fields

Revision ID: 04a533a9ac68
Revises: 2f4a4f2c7a8d
Create Date: 2024-01-23 17:24:02.764411-08:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '04a533a9ac68'
down_revision = '2f4a4f2c7a8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program_rule',
    sa.Column('uuid', sa.String(length=56), nullable=False),
    sa.Column('company_id', mysql.INTEGER(), nullable=False),
    sa.Column('rule_name', sa.String(length=255), nullable=False),
    sa.Column('rule_type', sa.String(length=56), nullable=False),
    sa.Column('cadence', sa.String(length=56), nullable=False),
    sa.Column('cadence_type', sa.String(length=56), nullable=False),
    sa.Column('cadence_value', sa.JSON(), nullable=False),
    sa.Column('trigger_field', sa.String(length=56), nullable=False),
    sa.Column('timing_type', sa.String(length=56), nullable=False),
    sa.Column('sending_time', sa.String(length=56), nullable=False),
    sa.Column('timezone', sa.String(length=56), nullable=False),
    sa.Column('manager_id', mysql.INTEGER(), nullable=False),
    sa.Column('sending_managers_account_id', mysql.INTEGER(), nullable=False),
    sa.Column('sending_managers_program_id', mysql.INTEGER(), nullable=False),
    sa.Column('bucket_customization_id', mysql.INTEGER(), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('memo', sa.String(length=255), nullable=False),
    sa.Column('recipient_note', sa.String(length=255), nullable=False),
    sa.Column('company_values', sa.JSON(), nullable=False),
    sa.Column('created_by', mysql.INTEGER(), nullable=False),
    sa.Column('updated_by', mysql.INTEGER(), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_index(op.f('ix_program_rule_cadence'), 'program_rule', ['cadence'], unique=False)
    op.create_index(op.f('ix_program_rule_cadence_type'), 'program_rule', ['cadence_type'], unique=False)
    op.create_index(op.f('ix_program_rule_company_id'), 'program_rule', ['company_id'], unique=False)
    op.create_index(op.f('ix_program_rule_manager_id'), 'program_rule', ['manager_id'], unique=False)
    op.create_index(op.f('ix_program_rule_rule_name'), 'program_rule', ['rule_name'], unique=False)
    op.create_index(op.f('ix_program_rule_rule_type'), 'program_rule', ['rule_type'], unique=False)
    op.create_index(op.f('ix_program_rule_sending_managers_program_id'), 'program_rule', ['sending_managers_program_id'], unique=False)
    op.create_index(op.f('ix_program_rule_sending_time'), 'program_rule', ['sending_time'], unique=False)
    op.create_index(op.f('ix_program_rule_timing_type'), 'program_rule', ['timing_type'], unique=False)
    op.create_index(op.f('ix_program_rule_trigger_field'), 'program_rule', ['trigger_field'], unique=False)
    op.create_index(op.f('ix_program_rule_uuid'), 'program_rule', ['uuid'], unique=False)
    op.drop_index('ix_reward_company_id', table_name='reward')
    op.drop_index('ix_reward_uuid', table_name='reward')
    op.drop_table('reward')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reward',
    sa.Column('uuid', mysql.VARCHAR(length=56), nullable=False),
    sa.Column('company_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('rule', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False),
    sa.Column('users', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False),
    sa.Column('reward_info', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=False),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_reward_uuid', 'reward', ['uuid'], unique=False)
    op.create_index('ix_reward_company_id', 'reward', ['company_id'], unique=False)
    op.drop_index(op.f('ix_program_rule_uuid'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_trigger_field'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_timing_type'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_sending_time'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_sending_managers_program_id'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_rule_type'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_rule_name'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_manager_id'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_company_id'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_cadence_type'), table_name='program_rule')
    op.drop_index(op.f('ix_program_rule_cadence'), table_name='program_rule')
    op.drop_table('program_rule')
    # ### end Alembic commands ###
