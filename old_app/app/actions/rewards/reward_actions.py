import calendar
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from app.models.reward.reward_models import (
    RewardCreate,
    RewardUpdate,
    RewardUsersUpdate,
    AnniversaryType,
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
    "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
    "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
    "scp": "account",
    "aud": None,
    "jti": "6f3d0081-0f73-473c-b1ad-c6165661d969"
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
        users: dict = mock_user_accounts

        user_rails_rewards = await cls.create_rails_reward(users["accounts"], reward)

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
        # reward_update.rule.anniversary_type = reward_update.rule.anniversary_type.value
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
        anniversary_type = AnniversaryType(reward.rule["anniversary_type"])

        users_by_anniversary = defaultdict(list)

        for account in user_accounts:
            # Parse datetime strings coming from rails
            birthday = datetime.fromisoformat(account["birthday"])
            hired_on_date = datetime.fromisoformat(account["hired_on"])
            onboard_date = hired_on_date + timedelta(days=90)

            today = datetime.now(timezone(timedelta(hours=-8))).date()
            if anniversary_type.BIRTHDAY:
                next_anniversary = cls.calculate_next_anniversary(birthday, today)
            elif anniversary_type.HIRE_DATE:
                next_anniversary = cls.calculate_next_anniversary(hired_on_date, today)
            elif anniversary_type.ONBOARDING_DATE:
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
        # # For temp testing purposes only. Remove when rails post is fully implemented
        # mock = True
        # if mock:
        #     return mock_create_reward_response(company_id)
        # else:
        # header = RequestHeaders(Cookie="stagingJwtToken=")

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
