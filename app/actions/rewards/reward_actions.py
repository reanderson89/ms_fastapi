import calendar
import os
from collections import defaultdict
from datetime import datetime, timedelta

import requests

from app.actions.http.rails_api_requests import HttpRequests as RailsRequests
from app.models.reward.reward_models import (
    RewardCreate,
    RewardUpdate,
    RewardUser,
    RewardUsersUpdate,
)
from burp.models.reward import RewardModelDB
from burp.utils.auth_utils import access_token_creation
from burp.utils.base_crud import BaseCRUD


EMPLOYEE = {
    "email": "robby.ketchell@gmail.com",
    "first_name": "Robby",
    "last_name": "Ketchell"
}

TOKEN_DATA = {
    "company_gid": "6cdcf917-a0da-4445-93ec-d51d662c60c6",
    "sub": "dd3085e2-a6bd-4339-a7bb-9d06c0132c34",
    "scp": "account",
    "aud": None,
    "jti": "6f3d0081-0f73-473c-b1ad-c6165661d969"
}


class RewardActions:

    # ver. 1a create_reward, does not add reward to db
    # @classmethod
    # async def create_reward(cls, request: Request, reward_create: RewardCreate):
    #     return await RailsRequests.post(path='/api/v4/company/rewards', body={
    #         "employee": {
    #             "email": EMPLOYEE["email"],
    #             "first_name": EMPLOYEE["first_name"],
    #             "last_name": EMPLOYEE["last_name"]
    #         },
    #         "bucket_customization": {
    #             "id": reward_create.bucket_customization_id
    #         },
    #         "program": {
    #             "id": reward_create.sending_managers_program_id
    #         },
    #         "subject": reward_create.subject,
    #         "memo": reward_create.memo,
    #         "company_values": reward_create.company_values,
    #         "share_achievement_data": {
    #             "recipients_emails": reward_create.recipient_emails,
    #             "note": reward_create.recipient_note
    #         }
    #     })

    @staticmethod
    async def to_reward_db_model(reward_create: RewardCreate):
        return RewardModelDB(
            **reward_create.dict()
        )

    # ver. 1b create_reward, adds reward to db, fetches users from rails and updates reward in db.
    @classmethod
    async def create_reward(cls, reward_create: RewardCreate):
        db_model_reward = await cls.to_reward_db_model(reward_create)
        reward = await BaseCRUD.create(db_model_reward)
        rails_api = os.environ["RAILS_API"]
        jwt = await access_token_creation(TOKEN_DATA, True)
        rails_response = requests.get(f"{rails_api}/accounts?company={reward_create.company_id}", headers={"Cookie": f'stagingJwtToken={jwt["access_token"]}'}).json()
        if reward and not rails_response:
            return {"message": "Reward created, error fetching user from rails."}
        user_list = [RewardUser(**user) for user in rails_response["accounts"]]

        # TODO: fully integrate into create_rewards. user_rails_rewards needs to be passed to update_reward
        # user_rails_rewards = await cls.create_rails_reward(user_list, reward)

        updated_reward = await cls.update_reward(reward.company_id, reward.uuid, RewardUsersUpdate(company_id=reward.company_id, users=user_list))
        if not updated_reward:
            return {"message": "Reward created, error updating reward with users from rails."}
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
        response = await BaseCRUD.get_all_where(
            RewardModelDB,
            [RewardModelDB.company_id],
            pagination=False,
            distinct_column=RewardModelDB.company_id
        )
        return response

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

    @classmethod
    async def create_rails_reward(cls, user_accounts: list, reward: RewardModelDB):
        anniversary_type = reward.rule["anniversary_type"]

        users_by_anniversary = defaultdict(list)

        for account in user_accounts:
            # Parse datetime strings coming from rails
            birthday = datetime.fromisoformat(account["birthday"])
            hired_on_date = datetime.fromisoformat(account["hired_on"])
            onboard_date = hired_on_date + timedelta(days=90)

            today = datetime.now().date()
            if anniversary_type.BIRTHDAY:
                next_anniversary = cls.calculate_next_anniversary(birthday, today)
            elif anniversary_type.HIRE_DATE:
                next_anniversary = cls.calculate_next_anniversary(hired_on_date, today)
            elif anniversary_type.ONBOARDING_DATE:
                next_anniversary = cls.calculate_next_anniversary(onboard_date, today)

            users_by_anniversary[next_anniversary.strftime("%m-%d-%y")].append(account)

        for users in users_by_anniversary.values():
            for user in users:
                response = await cls.rails_post(user, reward, reward.company_id)
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
    async def rails_post(cls, user: dict, reward: RewardModelDB, company_id: int):
        # For temp testing purposes only. Remove when rails post is fully implemented
        return await cls.mock_rails_post(user, reward, company_id)

        # TODO: fully implement rails post request
        return await RailsRequests.post(path="/api/v4/company/rewards", body={
            "employee": {
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"]
            },
            "bucket_customization": {
                "id": reward.reward_info["bucket_customization_id"]
            },
            "program": {
                "id": reward.reward_info["sending_managers_program_id"]
            },
            "subject": reward.reward_info["subject"],
            "memo": reward.reward_info["memo"],
            "company_values": reward.company_values,
            "share_achievement_data": {
                "recipients_emails": user["email"],
                "note": reward.recipient_note
            }
        })

    # For temp testing purposes only. Remove when rails post is fully implemented
    @classmethod
    async def mock_rails_post(cls, user, reward, id):
        from faker import Faker
        fake = Faker()
        response = {
            "reward": {
                "id": fake.random_int(min=10000, max=99999),  # Generate a random id
                # "offering_id": None,
                # "completed_at": None,
                "created_at": fake.date_time_this_year().isoformat(),  # Generate a random datetime this year
                "updated_at": fake.date_time_this_year().isoformat(),  # Generate a random datetime this year
                "code": fake.pystr(),  # Generate a random string
                "employee_id": fake.random_int(min=10000, max=99999),  # Generate a random employee id
                # "day_of_week": None,
                # "how_soon": None,
                # "activity_at": None,
                # "user_notes": None,
                # "deleted_at": None,
                "token": fake.sha1(),  # Generate a random SHA1 hash
                "feedback_received": fake.boolean(),  # Generate a random boolean
                "memo": fake.sentence(),  # Generate a random sentence
                "subject": fake.sentence(),  # Generate a random sentence
                "company_values_showcased": [
                    fake.word(),  # Generate a random word
                    fake.word(),  # Generate a random word
                    fake.word()  # Generate a random word
                ],
                "company_id": id,  # Use the provided id
                "manager_id": fake.random_int(min=10000, max=99999),  # Generate a random manager id
                "state": "approved",
                # "redeemed_at": None,
                # "experience_description": None,
                # "reward_type_id": None,
                # "custom_fields": {},
                # "in_discussion": False,
                # "redemption_response_set_access_code": None,
                # "watchlist": False,
                # "denied_at": None,
                # "days_until_sent": None,
                # "days_until_redeemed": None,
                # "days_until_completed": None,
                # "lifetime_in_days": None,
                # "scheduled_at": None,
                # "sent_at": None,
                # "thirty_day_redemption": True,
                # "fully_paid": False,
                # "experience_location": None,
                "approved_at": fake.date_time_this_year().isoformat(),  # Generate a random datetime this year
                # "post_experience_feedback_response_set_access_code": None,
                # "last_approval_reminder_sent_at": None,
                # "fully_paid_date": None,
                # "story_feedback": None,
                # "attachments_url": None,
                # "skip_pre_experience_emails": False,
                # "story_anticipation": None,
                # "employee_location_id": None,
                # "feedback_sent_at": None,
                # "feedback_reminder_sent_at": None,
                # "story_rank": 2,
                # "last_reset_at": None,
                # "deletion_reason": "",
                # "deprecated_deletion_approver": "",
                # "scheduling_at": None,
                # "number_of_people": None,
                # "days_until_activated": None,
                # "activated_at": None,
                # "private_note": "",
                # "flagged": False,
                # "total_expenses": "0.0",
                # "total_customer_reimbursements": "0.0",
                # "custom_priority": None,
                # "selected_location_id": None,
                # "redemption_blocker_survey_response_set_access_code": None,
                # "blocker_reminder_sent_at": None,
                # "calendar_event_id": None,
                # "calendar_invite_sent_at": None,
                # "program_id": 68,
                # "confirmation_email_sent_at": None,
                # "deletion_requested_at": None,
                # "deletion_approver_id": None,
                # "withdrawal_accounting_entity_id": 36853,
                # "place_id": None,
                # "provider_id": None,
                # "skip_blocker_reminder": False,
                # "accepted_legal_liability": None,
                # "skip_post_experience_emails": False,
                # "calendly_call_at": None,
                # "story_internal_note": None,
                # "scheduling_activated": True,
                # "employee_account_id": 30561,
                # "send_as_company": False,
                # "parent_id": None,
                # "accounting_combined": False,
                # "activity_at_time_zone": None,
                # "gid": "b882d7d9-2b48-4bb0-ac8f-00be2815f565",
                # "days_until_scheduled": None,
                # "gif_url": None,
                # "story_images_url": None
            }
        }

        return response
