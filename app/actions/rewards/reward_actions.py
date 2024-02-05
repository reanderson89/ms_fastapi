import calendar
import asyncio
from app.exceptions import ExceptionHandling
from datetime import datetime, timedelta, timezone
from app.worker.temp_worker import TempWorker
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from app.models.reward.reward_models import (
    ProgramRuleCreate,
    ProgramRuleUpdate,
    RuleType,
    StagedRewardCreate,
    SegmentRuleCreate,
    ProgramRuleRewardCountResponse
)
from burp.models.reward import ProgramRuleModelDB, StagedRewardModelDB, SegmentRuleModelDB, ProgramRuleModel
from burp.utils.base_crud import BaseCRUD

from app.models.rails import (
    RailsEmployee,
    RailsProgram,
    RailsBucketCustomization,
    RailsAchievementData,
    CreateRewardRequest
)
# from app.actions.rewards.mock_responses import mock_user_accounts
from burp.utils.auth_utils import access_token_creation
import os
import json
from requests.models import Response
from app.actions.rewards.mock_responses import mock_create_reward_response

# used for local development and testing
MOCK = os.environ.get("MOCK", "True").lower() == "true"


TOKEN_DATA = {
  "exp": 1707160158,
  "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
  "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
  "scp": "account",
  "aud": None,
  "iat": 1706900958,
  "jti": "235a312a-be28-4bdd-81ef-a047213ef24c"
}


class RuleActions:

    @staticmethod
    async def to_program_rule_db_model(rule_create: ProgramRuleCreate):
        return ProgramRuleModelDB(
            **rule_create.dict()
        )

    @classmethod
    async def create_rule(cls, rule_create: ProgramRuleCreate):
        rule = await cls.to_program_rule_db_model(rule_create)
        rule = await BaseCRUD.create(rule)
        if not rule:
            raise ExceptionHandling.custom400("Rule was not created.")
        worker = TempWorker()
        worker.get_users_for_reward_creation(rule)
        return rule

    @staticmethod
    async def get_program_rules_by_company(company_id, filter_params: dict = None):
        return await BaseCRUD.get_all_where(
            ProgramRuleModelDB,
            [ProgramRuleModelDB.company_id == company_id],
            params=filter_params,
            pagination=False
        )

    @staticmethod
    async def get_distinct_company_ids():
        return await BaseCRUD.get_all_where(
            ProgramRuleModelDB,
            [ProgramRuleModelDB.company_id],
            pagination=False,
            distinct_column=ProgramRuleModelDB.company_id
        )

    @staticmethod
    async def get_program_rule(company_id, rule_uuid):
        return await BaseCRUD.get_one_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ]
        )
    
    @staticmethod
    async def get_reward_count_for_rule(company_id, rule_uuid):
        count = await BaseCRUD.get_row_count(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.company_id == company_id
            ]
        )
        return ProgramRuleRewardCountResponse(
            staged_rewards=count,
            company_id=company_id,
            rule_uuid=rule_uuid
        )

    @staticmethod
    async def update_program_rule(company_id, rule_uuid, rule_update: ProgramRuleUpdate):
        return await BaseCRUD.update(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ],
            rule_update
        )

    @staticmethod
    async def delete_program_rule(company_id, rule_uuid):
        return await BaseCRUD.delete_one(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ]
        )

    @staticmethod
    async def get_headers():
        jwt = await access_token_creation(TOKEN_DATA, True)
        headers = {
            "Cookie": f"stagingJwtToken={jwt['access_token']}"
        }

        return headers

    @classmethod
    async def create_rails_reward(cls, user: dict, program_rule: ProgramRuleModel):
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

        rails_reward_response = await cls.rails_reward_request(user, program_rule)
        if not rails_reward_response.status_code == 200:
            raise Exception(rails_reward_response)
        
        rails_reward = rails_reward_response.json()
        user_reward = {
            "send_on": next_anniversary.strftime("%m-%d-%y"),
            **user,
            **rails_reward["reward"]
        }
        staged_reward = await cls.create_staged_reward(user_reward, program_rule.uuid)


        return staged_reward

    @staticmethod
    def calculate_next_anniversary(date, today):
        # Special case for February 29
        if date.month == 2 and date.day == 29 and not calendar.isleap(today.year):
            next_anniversary = datetime(today.year, 3, 1).date()
        else:
            next_anniversary = date.replace(year=today.year) if date.month > today.month or (date.month == today.month and date.day >= today.day) else date.replace(year=today.year + 1)
        return next_anniversary

    @classmethod
    async def rails_reward_request(cls, user: dict, program_rule: ProgramRuleModelDB):
        if MOCK:
            # return mock rails reward object
            response = mock_create_reward_response(program_rule.company_id)
            response_obj = Response()
            response_obj.status_code = 200
            response_obj._content = json.dumps(response).encode("utf-8")
            return response_obj
        else:
            employee = RailsEmployee(
                email=user["email"],
                first_name=user["first_name"],
                last_name=user["last_name"]
            )
            bucket_customization = RailsBucketCustomization(
                id=program_rule.bucket_customization_id
            )
            program = RailsProgram(
                id=program_rule.sending_managers_program_id
            )
            share_achievement_data = RailsAchievementData(
                recipients_emails=[user["email"]],
                note=program_rule.recipient_note
            )
            create_reward = CreateRewardRequest(
                employee=employee,
                bucket_customization=bucket_customization,
                program=program,
                subject=program_rule.subject,
                memo=program_rule.memo,
                share_achievement_data=share_achievement_data,
                company_values=program_rule.company_values
            )

            return await RailsRequests.post(
                path="/api/v4/company/rewards",
                headers=await cls.get_headers(),
                body=create_reward.dict()
            )

    @staticmethod
    async def create_staged_reward(reward: dict, rule_uuid: str):
        reward_data = StagedRewardCreate(
            **reward,
            reward_id=reward.get("id"),
            rule_uuid=rule_uuid
        )
        db_reward = StagedRewardModelDB(**reward_data.dict())
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
