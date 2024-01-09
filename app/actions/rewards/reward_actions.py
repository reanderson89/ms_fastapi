import calendar
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from app.worker.temp_worker import TempWorker
from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from app.models.reward.reward_models import (
    RewardCreate,
    RewardUpdate,
    RewardUsersUpdate,
    RuleType,
    # RewardUser,
)
from burp.models.reward import RewardModelDB
from burp.utils.base_crud import BaseCRUD

from app.models.rails import (
    RailsEmployee,
    RailsProgram,
    RailsBucketCustomization,
    RailsAchievementData,
    CreateRewardRequest
)
from app.actions.rewards.mock_responses import mock_user_accounts
from burp.utils.auth_utils import access_token_creation

TOKEN_DATA = {
  "exp": 1704734963,
  "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
  "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
  "scp": "account",
  "aud": None,
  "iat": 1704475763,
  "jti": "6273b5ae-c2f8-4390-b694-c484362e4ce8"
}



class RewardActions:

    @staticmethod
    async def to_reward_db_model(reward_create: RewardCreate):
        return RewardModelDB(
            **reward_create.dict()
        )

    @classmethod
    async def create_reward(cls, reward_create: RewardCreate):
        db_model_reward = await cls.to_reward_db_model(reward_create)
        reward = await BaseCRUD.create(db_model_reward)

        # TODO: Get Users
        # users = await RailsRequests.get(path=f"/accounts?company={reward_create.company_id}")
        # users: dict = mock_user_accounts
        worker = TempWorker()
        users = await worker.get_users_by_company_id(reward_create.company_id)

        user_rails_rewards = await cls.create_rails_reward(users, reward)

        updated_reward = await cls.update_reward(
            reward.company_id,
            reward.uuid,
            RewardUsersUpdate(company_id=reward.company_id, users=dict(user_rails_rewards))
        )
        if not updated_reward:
            return {"message": "Rewards created, error updating reward with users and rewards from rails."}
        return updated_reward

    @classmethod
    async def get_rewards_by_company(cls, company_id, filter_params: dict = None):
        return await BaseCRUD.get_all_where(
            RewardModelDB,
            [RewardModelDB.company_id == company_id],
            params=filter_params,
            pagination=False
        )

    @classmethod
    async def get_distinct_company_ids(cls):
        return await BaseCRUD.get_all_where(
            RewardModelDB,
            [RewardModelDB.company_id],
            pagination=False,
            distinct_column=RewardModelDB.company_id
        )

    @classmethod
    async def get_reward(cls, company_id, reward_uuid):
        return await BaseCRUD.get_one_where(
            RewardModelDB,
            [
                RewardModelDB.company_id == company_id,
                RewardModelDB.uuid == reward_uuid
            ]
        )

    @classmethod
    async def update_reward(cls, company_id, reward_uuid, reward_update: RewardUpdate):
        # reward_update.rule.rule_type = reward_update.rule.rule_type.value
        return await BaseCRUD.update(
            RewardModelDB,
            [
                RewardModelDB.company_id == company_id,
                RewardModelDB.uuid == reward_uuid
            ],
            reward_update
        )

    @classmethod
    async def delete_reward(cls, company_id, reward_uuid):
        return await BaseCRUD.delete_one(
            RewardModelDB,
            [
                RewardModelDB.company_id == company_id,
                RewardModelDB.uuid == reward_uuid
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
    async def create_rails_reward(cls, user_accounts: list, reward: RewardModelDB):
        rule_type = RuleType(reward.rule["rule_type"])

        users_by_anniversary = defaultdict(list)

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

            users_by_anniversary[next_anniversary.strftime("%m-%d-%y")].append(account)

        for users in users_by_anniversary.values():
            for user in users:
                response = (await cls.rails_reward_request(user, reward, reward.company_id)).json()
                user["reward"] = response["reward"]

        return users_by_anniversary

    @staticmethod
    def calculate_next_anniversary(date, today):
        # Special case for February 29
        if date.month == 2 and date.day == 29 and not calendar.isleap(today.year):
            next_anniversary = datetime(today.year, 3, 1).date()
        else:
            next_anniversary = date.replace(year=today.year) if date.month > today.month or (date.month == today.month and date.day >= today.day) else date.replace(year=today.year + 1)
        return next_anniversary

    @classmethod
    async def rails_reward_request(cls, user: dict, reward: RewardModelDB, company_id: int = None):
        # For temp FE testing purposes
        import os
        import json
        from requests.models import Response
        from app.actions.rewards.mock_responses import mock_create_reward_response

        MOCK = os.environ.get("MOCK", "True").lower() == "true"
        if MOCK:
            # put in to json format
            response = mock_create_reward_response(company_id)
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
                id=reward.reward_info["bucket_customization"]
            )
            program = RailsProgram(
                id=reward.reward_info["sending_managers_program_id"]
            )
            share_achievement_data = RailsAchievementData(
                recipients_emails=[user["email"]],
                note=reward.reward_info["recipient_note"]
            )
            create_reward = CreateRewardRequest(
                employee=employee,
                bucket_customization=bucket_customization,
                program=program,
                subject=reward.reward_info["subject"],
                memo=reward.reward_info["memo"],
                share_achievement_data=share_achievement_data,
                company_values=reward.reward_info["company_values"]
            )

            return await RailsRequests.post(
                path="/api/v4/company/rewards",
                headers=await cls.get_headers(),
                body=create_reward.dict()
            )
