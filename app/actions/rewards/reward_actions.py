from fastapi import Request

from app.models.reward.reward_models import RewardCreate, RewardUpdate, RewardUser, RewardUsersUpdate
from burp.models.reward import RewardModelDB
from burp.utils.base_crud import BaseCRUD
from burp.utils.auth_utils import access_token_creation

from ..http.rails_api_requests import HttpRequests as RailsRequests

EMPLOYEE = {
    'email': 'robby.ketchell@gmail.com',
    'first_name': 'Robby',
    'last_name': 'Ketchell'
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
    @classmethod
    async def create_reward(cls, request: Request, reward_create: RewardCreate):
        return await RailsRequests.post(path='/api/v4/company/rewards', body={
            "employee": {
                "email": EMPLOYEE["email"],
                "first_name": EMPLOYEE["first_name"],
                "last_name": EMPLOYEE["last_name"]
            },
            "bucket_customization": {
                "id": reward_create.bucket_customization_id
            },
            "program": {
                "id": reward_create.sending_managers_program_id
            },
            "subject": reward_create.subject,
            "memo": reward_create.memo,
            "company_values": reward_create.company_values,
            "share_achievement_data": {
                "recipients_emails": reward_create.recipient_emails,
                "note": reward_create.recipient_note
            }
        })

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
            return {"message":"Reward created, error fetching user from rails."}
        user_list = [RewardUser(**user) for user in rails_response['accounts']]
        # POST req o rails to create rewards. Being completed by Josh
        updated_reward = await cls.update_reward(reward.company_id, reward.uuid, RewardUsersUpdate(company_id=reward.company_id, users=user_list))
        if not updated_reward:
            return {"message": "Reward created, error updating reward with users from rails."}
        return updated_reward

    @classmethod
    async def get_rewards_by_company(cls, company_id, fitler_params: dict = None):
        return await BaseCRUD.get_all_where(
            RewardModelDB,
            [RewardModelDB.company_id == company_id],
            params=fitler_params,
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
