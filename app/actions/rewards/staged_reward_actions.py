import calendar
from datetime import datetime, timedelta, timezone
from app.models.reward.reward_models import (
    RuleType,
    StagedRewardUpdate,
    RewardState,
)
from burp.models.reward import StagedRewardModelDB, ProgramRuleModel
from burp.utils.base_crud import BaseCRUD
from app.worker.logging_format import init_logger

logger = init_logger()


class StagedRewardActions:
    
    @staticmethod
    async def to_staged_reward_db_model(user: dict, rule: ProgramRuleModel, send_on: str):
        return StagedRewardModelDB(
            user_account_uuid=user['user_account_uuid'],
            employee_id=user['employee_id'],
            company_id=rule.company_id,
            state=RewardState.STAGED.value,
            rule_uuid=rule.uuid,
            employee_account_id=user['account_id'],
            gid=user['account_gid'],
            program_id=rule.sending_managers_program_id,
            bucket_customization_id=rule.bucket_customization_id,
            bucket_customization_price=rule.bucket_customization_price,
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email'],
            send_on=send_on
        )

    @staticmethod
    async def handle_delete_staged_rewards(company_id: int, rule_uuid: str):
        return await BaseCRUD.delete_all(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.company_id == company_id,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ]
        )
        
    @staticmethod
    async def update_staged_reward(staged_reward_uuid: str, company_id: int, rule_uuid: str, staged_reward_update: StagedRewardUpdate):
        return await BaseCRUD.update(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.uuid == staged_reward_uuid,
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.company_id == company_id
            ],
            staged_reward_update
        )

    @classmethod
    async def get_send_time(cls, user: dict, program_rule: ProgramRuleModel):
        rule_type = RuleType(program_rule.rule_type)

        # Parse datetime strings coming from rails
        birthday = datetime.fromtimestamp(user["time_birthday"])
        hired_on_date = datetime.fromtimestamp(user["hired_on"])
        onboard_date = hired_on_date + timedelta(days=90)

        today = datetime.now(timezone(timedelta(hours=-8))).date()
        if rule_type.BIRTHDAY:
            next_anniversary = cls.calculate_next_anniversary(birthday, today)
        elif rule_type.ANNIVERSARY:
            next_anniversary = cls.calculate_next_anniversary(hired_on_date, today)
        elif rule_type.ONBOARDING:
            next_anniversary = cls.calculate_next_anniversary(onboard_date, today)

        return next_anniversary.strftime("%m-%d-%y")

    @staticmethod
    def calculate_next_anniversary(date: datetime, today: datetime):
        # Special case for February 29
        if date.month == 2 and date.day == 29 and not calendar.isleap(today.year):
            next_anniversary = datetime(today.year, 3, 1).date()
        else:
            next_anniversary = date.replace(year=today.year) if date.month > today.month or (date.month == today.month and date.day >= today.day) else date.replace(year=today.year + 1)
        return next_anniversary

    @classmethod
    async def create_staged_reward(cls, user: dict, rule: ProgramRuleModel):
        send_on = await cls.get_send_time(user, rule)
        db_reward = await cls.to_staged_reward_db_model(user, rule, send_on)
        return await BaseCRUD.create(db_reward)

    @staticmethod
    async def get_staged_rewards_by_date(rule_uuid: int, date: str):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.send_on == date
            ],
            pagination=False
        )
    
    @staticmethod 
    async def get_staged_rewards_by_rule(company_id: int, rule_uuid: str):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.company_id == company_id,
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ],
            pagination=False
        )
