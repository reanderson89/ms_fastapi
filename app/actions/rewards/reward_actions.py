import calendar
from datetime import datetime, timedelta, timezone
from app.worker.temp_worker import TempWorker
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from app.models.reward.reward_models import (
    ProgramRuleCreate,
    ProgramRuleUpdate,
    RuleType,
    StagedRewardCreate,
    # SegmentRuleCreate
)
from burp.models.reward import ProgramRuleModelDB, StagedRewardModelDB  #, SegmentRuleModelDB
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
    "exp": 1704734963,
    "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
    "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
    "scp": "account",
    "aud": None,
    "iat": 1704475763,
    "jti": "6273b5ae-c2f8-4390-b694-c484362e4ce8"
}


class RuleActions:

    @staticmethod
    async def to_program_rule_db_model(rule_create: ProgramRuleCreate):
        return ProgramRuleModelDB(
            **rule_create.dict(exclude={"segment_by"})
        )

    # @staticmethod
    # async def to_segment_rule_db_model(segment_rule_create: SegmentRuleCreate):
    #     return SegmentRuleModelDB(
    #         **segment_rule_create.dict()
    #     )

    @classmethod
    async def create_rule(cls, rule_create: ProgramRuleCreate):
        # TODO: values from rule_create.segmented_by need to be handled
        db_program_rule = await cls.to_program_rule_db_model(rule_create)
        program_rule = await BaseCRUD.create(db_program_rule)

        # TODO: add cadence & segmentation logic
        worker = TempWorker()
        users = await worker.get_users_by_company_id(rule_create.company_id)

        rails_rewards = await cls.create_rails_reward(users, program_rule)

        staged_rewards = [await cls.create_staged_reward(reward, program_rule.uuid) for reward in rails_rewards]

        if not staged_rewards:
            return {"message": "Rewards created, error creating staged rewards."}
        return program_rule

    @classmethod
    async def get_program_rules_by_company(cls, company_id, filter_params: dict = None):
        return await BaseCRUD.get_all_where(
            ProgramRuleModelDB,
            [ProgramRuleModelDB.company_id == company_id],
            params=filter_params,
            pagination=False
        )

    @classmethod
    async def get_distinct_company_ids(cls):
        return await BaseCRUD.get_all_where(
            ProgramRuleModelDB,
            [ProgramRuleModelDB.company_id],
            pagination=False,
            distinct_column=ProgramRuleModelDB.company_id
        )

    @classmethod
    async def get_program_rule(cls, company_id, rule_uuid):
        return await BaseCRUD.get_one_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ]
        )

    @classmethod
    async def update_program_rule(cls, company_id, rule_uuid, rule_update: ProgramRuleUpdate):
        return await BaseCRUD.update(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ],
            rule_update
        )

    @classmethod
    async def delete_program_rule(cls, company_id, rule_uuid):
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
    async def create_rails_reward(cls, user_accounts: list, program_rule: ProgramRuleModelDB):
        rule_type = RuleType(program_rule.rule_type)

        user_rewards = list()

        for account in user_accounts:
            # Parse datetime strings coming from rails
            birthday = datetime.fromtimestamp(account["time_birthday"])
            hired_on_date = datetime.fromtimestamp(account["hired_on"])
            onboard_date = hired_on_date + timedelta(days=90)

            today = datetime.now(timezone(timedelta(hours=-8))).date()
            if rule_type.BIRTHDAY:
                next_anniversary = cls.calculate_next_anniversary(birthday, today)
            elif rule_type.HIRE_DATE:
                next_anniversary = cls.calculate_next_anniversary(hired_on_date, today)
            elif rule_type.ONBOARDING_DATE:
                next_anniversary = cls.calculate_next_anniversary(onboard_date, today)

            rails_reward = (await cls.rails_reward_request(account, program_rule)).json()

            # staged_reward = await cls.create_staged_reward(program_rule)

            user_rewards.append({
                "send_on": next_anniversary.strftime("%m-%d-%y"),
                **account,
                **rails_reward["reward"]
            })

        return user_rewards

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

    @classmethod
    async def create_staged_reward(cls, reward: dict, rule_uuid: str):
        reward_data = StagedRewardCreate(
            **reward,
            reward_id=reward.get("id"),
            rule_uuid=rule_uuid
        )
        db_reward = StagedRewardModelDB(**reward_data.dict())
        return await BaseCRUD.create(db_reward)

    @classmethod
    async def get_staged_rewards_by_date(cls, rule_uuid: int, date: str):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.send_on == date
            ],
            pagination=False
        )
