"""removes old milestones tables

Revision ID: 0e34f44d229c
Revises: a170534ed314
Create Date: 2024-01-02 16:36:28.043487

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0e34f44d229c'
down_revision = 'a170534ed314'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_program_budget_9char', table_name='program')
    op.drop_index('ix_program_cadence', table_name='program')
    op.drop_index('ix_program_cadence_value', table_name='program')
    op.drop_index('ix_program_client_uuid', table_name='program')
    op.drop_index('ix_program_description', table_name='program')
    op.drop_index('ix_program_name', table_name='program')
    op.drop_index('ix_program_program_9char', table_name='program')
    op.drop_index('ix_program_program_type', table_name='program')
    op.drop_index('ix_program_status', table_name='program')
    op.drop_index('ix_program_user_uuid', table_name='program')
    op.drop_index('ix_program_uuid', table_name='program')
    op.drop_table('program')
    op.drop_index('ix_client_budget_budget_9char', table_name='client_budget')
    op.drop_index('ix_client_budget_client_uuid', table_name='client_budget')
    op.drop_index('ix_client_budget_parent_9char', table_name='client_budget')
    op.drop_index('ix_client_budget_uuid', table_name='client_budget')
    op.drop_table('client_budget')
    op.drop_index('ix_client_user_client_uuid', table_name='client_user')
    op.drop_index('ix_client_user_employee_id', table_name='client_user')
    op.drop_index('ix_client_user_manager_uuid', table_name='client_user')
    op.drop_index('ix_client_user_user_uuid', table_name='client_user')
    op.drop_index('ix_client_user_uuid', table_name='client_user')
    op.drop_table('client_user')
    op.drop_index('ix_program_award_client_uuid', table_name='program_award')
    op.drop_index('ix_program_award_uuid', table_name='program_award')
    op.drop_table('program_award')
    op.drop_index('ix_award_award_type', table_name='award')
    op.drop_index('ix_award_channel', table_name='award')
    op.drop_index('ix_award_hero_image', table_name='award')
    op.drop_index('ix_award_name', table_name='award')
    op.drop_index('ix_award_uuid', table_name='award')
    op.drop_index('ix_award_value', table_name='award')
    op.drop_table('award')
    op.drop_table('program_segment_award')
    op.drop_index('ix_program_segment_rule_client_uuid', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_logic', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_program_9char', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_program_uuid', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_rule_9char', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_rule_type', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_segment_9char', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_status', table_name='program_segment_rule')
    op.drop_index('ix_program_segment_rule_uuid', table_name='program_segment_rule')
    op.drop_table('program_segment_rule')
    op.drop_index('ix_client_award_client_uuid', table_name='client_award')
    op.drop_index('ix_client_award_uuid', table_name='client_award')
    op.drop_table('client_award')
    op.drop_index('ix_program_rule_client_uuid', table_name='program_rule')
    op.drop_index('ix_program_rule_logic', table_name='program_rule')
    op.drop_index('ix_program_rule_program_9char', table_name='program_rule')
    op.drop_index('ix_program_rule_program_uuid', table_name='program_rule')
    op.drop_index('ix_program_rule_rule_9char', table_name='program_rule')
    op.drop_index('ix_program_rule_rule_type', table_name='program_rule')
    op.drop_index('ix_program_rule_status', table_name='program_rule')
    op.drop_index('ix_program_rule_uuid', table_name='program_rule')
    op.drop_table('program_rule')
    op.drop_index('ix_message_client_uuid', table_name='message')
    op.drop_index('ix_message_message_9char', table_name='message')
    op.drop_index('ix_message_message_uuid', table_name='message')
    op.drop_index('ix_message_program_9char', table_name='message')
    op.drop_index('ix_message_segment_9char', table_name='message')
    op.drop_index('ix_message_uuid', table_name='message')
    op.drop_table('message')
    op.drop_index('ix_program_admin_client_uuid', table_name='program_admin')
    op.drop_index('ix_program_admin_permissions', table_name='program_admin')
    op.drop_index('ix_program_admin_program_9char', table_name='program_admin')
    op.drop_index('ix_program_admin_program_uuid', table_name='program_admin')
    op.drop_index('ix_program_admin_user_uuid', table_name='program_admin')
    op.drop_index('ix_program_admin_uuid', table_name='program_admin')
    op.drop_table('program_admin')
    op.drop_index('ix_program_segment_budget_9char', table_name='program_segment')
    op.drop_index('ix_program_segment_client_uuid', table_name='program_segment')
    op.drop_index('ix_program_segment_program_9char', table_name='program_segment')
    op.drop_index('ix_program_segment_segment_9char', table_name='program_segment')
    op.drop_index('ix_program_segment_status', table_name='program_segment')
    op.drop_index('ix_program_segment_uuid', table_name='program_segment')
    op.drop_table('program_segment')
    op.drop_index('ix_client_description', table_name='client')
    op.drop_index('ix_client_name', table_name='client')
    op.drop_index('ix_client_url', table_name='client')
    op.drop_index('ix_client_uuid', table_name='client')
    op.drop_table('client')
    op.drop_index('ix_program_segment_design_channel', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_client_uuid', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_design_9char', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_message_uuid', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_program_9char', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_program_uuid', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_segment_9char', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_status', table_name='program_segment_design')
    op.drop_index('ix_program_segment_design_uuid', table_name='program_segment_design')
    op.drop_table('program_segment_design')
    op.drop_index('ix_program_event_client_uuid', table_name='program_event')
    op.drop_index('ix_program_event_event_9char', table_name='program_event')
    op.drop_index('ix_program_event_event_type', table_name='program_event')
    op.drop_index('ix_program_event_parent_9char', table_name='program_event')
    op.drop_index('ix_program_event_program_9char', table_name='program_event')
    op.drop_index('ix_program_event_program_uuid', table_name='program_event')
    op.drop_index('ix_program_event_segment_9char', table_name='program_event')
    op.drop_index('ix_program_event_status', table_name='program_event')
    op.drop_index('ix_program_event_uuid', table_name='program_event')
    op.drop_table('program_event')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program_event',
    sa.Column('uuid', mysql.VARCHAR(length=72), nullable=False),
    sa.Column('program_uuid', mysql.VARCHAR(length=65), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('event_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('event_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('parent_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('event_data', mysql.TEXT(), nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_event_uuid', 'program_event', ['uuid'], unique=False)
    op.create_index('ix_program_event_status', 'program_event', ['status'], unique=False)
    op.create_index('ix_program_event_segment_9char', 'program_event', ['segment_9char'], unique=False)
    op.create_index('ix_program_event_program_uuid', 'program_event', ['program_uuid'], unique=False)
    op.create_index('ix_program_event_program_9char', 'program_event', ['program_9char'], unique=False)
    op.create_index('ix_program_event_parent_9char', 'program_event', ['parent_9char'], unique=False)
    op.create_index('ix_program_event_event_type', 'program_event', ['event_type'], unique=False)
    op.create_index('ix_program_event_event_9char', 'program_event', ['event_9char'], unique=False)
    op.create_index('ix_program_event_client_uuid', 'program_event', ['client_uuid'], unique=False)
    op.create_table('program_segment_design',
    sa.Column('uuid', mysql.VARCHAR(length=81), nullable=False),
    sa.Column('program_uuid', mysql.VARCHAR(length=65), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('design_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('message_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('channel', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_segment_design_uuid', 'program_segment_design', ['uuid'], unique=False)
    op.create_index('ix_program_segment_design_status', 'program_segment_design', ['status'], unique=False)
    op.create_index('ix_program_segment_design_segment_9char', 'program_segment_design', ['segment_9char'], unique=False)
    op.create_index('ix_program_segment_design_program_uuid', 'program_segment_design', ['program_uuid'], unique=False)
    op.create_index('ix_program_segment_design_program_9char', 'program_segment_design', ['program_9char'], unique=False)
    op.create_index('ix_program_segment_design_message_uuid', 'program_segment_design', ['message_uuid'], unique=False)
    op.create_index('ix_program_segment_design_design_9char', 'program_segment_design', ['design_9char'], unique=False)
    op.create_index('ix_program_segment_design_client_uuid', 'program_segment_design', ['client_uuid'], unique=False)
    op.create_index('ix_program_segment_design_channel', 'program_segment_design', ['channel'], unique=False)
    op.create_table('client',
    sa.Column('uuid', mysql.VARCHAR(length=56), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('url', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_ping', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=4), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_client_uuid', 'client', ['uuid'], unique=False)
    op.create_index('ix_client_url', 'client', ['url'], unique=False)
    op.create_index('ix_client_name', 'client', ['name'], unique=False)
    op.create_index('ix_client_description', 'client', ['description'], unique=False)
    op.create_table('program_segment',
    sa.Column('uuid', mysql.VARCHAR(length=72), nullable=False),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('budget_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=4), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_segment_uuid', 'program_segment', ['uuid'], unique=False)
    op.create_index('ix_program_segment_status', 'program_segment', ['status'], unique=False)
    op.create_index('ix_program_segment_segment_9char', 'program_segment', ['segment_9char'], unique=False)
    op.create_index('ix_program_segment_program_9char', 'program_segment', ['program_9char'], unique=False)
    op.create_index('ix_program_segment_client_uuid', 'program_segment', ['client_uuid'], unique=False)
    op.create_index('ix_program_segment_budget_9char', 'program_segment', ['budget_9char'], unique=False)
    op.create_table('program_admin',
    sa.Column('uuid', mysql.VARCHAR(length=56), nullable=False),
    sa.Column('program_uuid', mysql.VARCHAR(length=65), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('user_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('permissions', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_admin_uuid', 'program_admin', ['uuid'], unique=False)
    op.create_index('ix_program_admin_user_uuid', 'program_admin', ['user_uuid'], unique=False)
    op.create_index('ix_program_admin_program_uuid', 'program_admin', ['program_uuid'], unique=False)
    op.create_index('ix_program_admin_program_9char', 'program_admin', ['program_9char'], unique=False)
    op.create_index('ix_program_admin_permissions', 'program_admin', ['permissions'], unique=False)
    op.create_index('ix_program_admin_client_uuid', 'program_admin', ['client_uuid'], unique=False)
    op.create_table('message',
    sa.Column('uuid', mysql.VARCHAR(length=83), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('message_uuid', mysql.VARCHAR(length=74), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('message_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('message_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('channel', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('body', mysql.TEXT(), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_message_uuid', 'message', ['uuid'], unique=False)
    op.create_index('ix_message_segment_9char', 'message', ['segment_9char'], unique=False)
    op.create_index('ix_message_program_9char', 'message', ['program_9char'], unique=False)
    op.create_index('ix_message_message_uuid', 'message', ['message_uuid'], unique=False)
    op.create_index('ix_message_message_9char', 'message', ['message_9char'], unique=False)
    op.create_index('ix_message_client_uuid', 'message', ['client_uuid'], unique=False)
    op.create_table('program_rule',
    sa.Column('uuid', mysql.VARCHAR(length=81), nullable=False),
    sa.Column('program_uuid', mysql.VARCHAR(length=65), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('rule_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('rule_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('logic', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_rule_uuid', 'program_rule', ['uuid'], unique=False)
    op.create_index('ix_program_rule_status', 'program_rule', ['status'], unique=False)
    op.create_index('ix_program_rule_rule_type', 'program_rule', ['rule_type'], unique=False)
    op.create_index('ix_program_rule_rule_9char', 'program_rule', ['rule_9char'], unique=False)
    op.create_index('ix_program_rule_program_uuid', 'program_rule', ['program_uuid'], unique=False)
    op.create_index('ix_program_rule_program_9char', 'program_rule', ['program_9char'], unique=False)
    op.create_index('ix_program_rule_logic', 'program_rule', ['logic'], unique=False)
    op.create_index('ix_program_rule_client_uuid', 'program_rule', ['client_uuid'], unique=False)
    op.create_table('client_award',
    sa.Column('uuid', mysql.VARCHAR(length=65), nullable=False),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('client_award_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('award_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('hero_image', mysql.VARCHAR(length=4), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_client_award_uuid', 'client_award', ['uuid'], unique=False)
    op.create_index('ix_client_award_client_uuid', 'client_award', ['client_uuid'], unique=False)
    op.create_table('program_segment_rule',
    sa.Column('uuid', mysql.VARCHAR(length=81), nullable=False),
    sa.Column('program_uuid', mysql.VARCHAR(length=65), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('rule_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('rule_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('logic', mysql.LONGTEXT(charset='utf8mb4', collation='utf8mb4_bin'), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_segment_rule_uuid', 'program_segment_rule', ['uuid'], unique=False)
    op.create_index('ix_program_segment_rule_status', 'program_segment_rule', ['status'], unique=False)
    op.create_index('ix_program_segment_rule_segment_9char', 'program_segment_rule', ['segment_9char'], unique=False)
    op.create_index('ix_program_segment_rule_rule_type', 'program_segment_rule', ['rule_type'], unique=False)
    op.create_index('ix_program_segment_rule_rule_9char', 'program_segment_rule', ['rule_9char'], unique=False)
    op.create_index('ix_program_segment_rule_program_uuid', 'program_segment_rule', ['program_uuid'], unique=False)
    op.create_index('ix_program_segment_rule_program_9char', 'program_segment_rule', ['program_9char'], unique=False)
    op.create_index('ix_program_segment_rule_logic', 'program_segment_rule', ['logic'], unique=False)
    op.create_index('ix_program_segment_rule_client_uuid', 'program_segment_rule', ['client_uuid'], unique=False)
    op.create_table('program_segment_award',
    sa.Column('uuid', mysql.VARCHAR(length=83), nullable=False),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('program_award_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('segment_award_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('client_award_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('hero_image', mysql.VARCHAR(length=4), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('award',
    sa.Column('uuid', mysql.VARCHAR(length=56), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('hero_image', mysql.VARCHAR(length=4), nullable=True),
    sa.Column('channel', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('award_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('value', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_award_value', 'award', ['value'], unique=False)
    op.create_index('ix_award_uuid', 'award', ['uuid'], unique=False)
    op.create_index('ix_award_name', 'award', ['name'], unique=False)
    op.create_index('ix_award_hero_image', 'award', ['hero_image'], unique=False)
    op.create_index('ix_award_channel', 'award', ['channel'], unique=False)
    op.create_index('ix_award_award_type', 'award', ['award_type'], unique=False)
    op.create_table('program_award',
    sa.Column('uuid', mysql.VARCHAR(length=74), nullable=False),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('program_award_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('client_award_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('hero_image', mysql.VARCHAR(length=4), nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_award_uuid', 'program_award', ['uuid'], unique=False)
    op.create_index('ix_program_award_client_uuid', 'program_award', ['client_uuid'], unique=False)
    op.create_table('client_user',
    sa.Column('uuid', mysql.VARCHAR(length=56), nullable=False),
    sa.Column('user_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('manager_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('employee_id', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('department', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_hire', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_start', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('admin', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_client_user_uuid', 'client_user', ['uuid'], unique=False)
    op.create_index('ix_client_user_user_uuid', 'client_user', ['user_uuid'], unique=False)
    op.create_index('ix_client_user_manager_uuid', 'client_user', ['manager_uuid'], unique=False)
    op.create_index('ix_client_user_employee_id', 'client_user', ['employee_id'], unique=False)
    op.create_index('ix_client_user_client_uuid', 'client_user', ['client_uuid'], unique=False)
    op.create_table('client_budget',
    sa.Column('uuid', mysql.VARCHAR(length=65), nullable=False),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('budget_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('parent_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('value', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.Column('budget_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_client_budget_uuid', 'client_budget', ['uuid'], unique=False)
    op.create_index('ix_client_budget_parent_9char', 'client_budget', ['parent_9char'], unique=False)
    op.create_index('ix_client_budget_client_uuid', 'client_budget', ['client_uuid'], unique=False)
    op.create_index('ix_client_budget_budget_9char', 'client_budget', ['budget_9char'], unique=False)
    op.create_table('program',
    sa.Column('uuid', mysql.VARCHAR(length=65), nullable=False),
    sa.Column('user_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('program_9char', mysql.VARCHAR(length=9), nullable=True),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('client_uuid', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('budget_9char', mysql.VARCHAR(length=56), nullable=True),
    sa.Column('status', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('program_type', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('cadence', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('cadence_value', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_created', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('time_updated', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_program_uuid', 'program', ['uuid'], unique=False)
    op.create_index('ix_program_user_uuid', 'program', ['user_uuid'], unique=False)
    op.create_index('ix_program_status', 'program', ['status'], unique=False)
    op.create_index('ix_program_program_type', 'program', ['program_type'], unique=False)
    op.create_index('ix_program_program_9char', 'program', ['program_9char'], unique=False)
    op.create_index('ix_program_name', 'program', ['name'], unique=False)
    op.create_index('ix_program_description', 'program', ['description'], unique=False)
    op.create_index('ix_program_client_uuid', 'program', ['client_uuid'], unique=False)
    op.create_index('ix_program_cadence_value', 'program', ['cadence_value'], unique=False)
    op.create_index('ix_program_cadence', 'program', ['cadence'], unique=False)
    op.create_index('ix_program_budget_9char', 'program', ['budget_9char'], unique=False)
    # ### end Alembic commands ###
