import os
import requests
from app.models.reward.reward_models import RewardCreate
from fastapi import Request
from burp.utils.base_crud import BaseCRUD
from burp.models.reward import RewardModelDB

import os
import requests


EMPLOYEE = {
    'email': 'katie.cunningham@blueboard.com',
    'first_name': 'Katie',
    'last_name': 'Cunningham'
}


class RewardActions:

    # ver. 1a create_reward, does not add reward to db
    @classmethod
    async def create_reward(cls, request: Request, reward_create: RewardCreate):
        rails_api = os.environ["RAILS_API"]
        url = f'{rails_api}/api/v4/company/rewards'
        response = requests.post(url=url, headers={
            'cookie': request.headers['cookie']
        }, json={
            'employee': {
                'email': EMPLOYEE['email'],
                'first_name': EMPLOYEE['first_name'],
                'last_name': EMPLOYEE['last_name']
            },
            'bucket_customization': {
                'id': reward_create.bucket_customization_id
            },
            'program': {
                'id': reward_create.sending_managers_program_id
            },
            'subject': reward_create.subject,
            'memo': reward_create.memo,
            'company_values': reward_create.company_values,
            'share_achievement_data': {
                'recipients_emails': reward_create.recipient_emails,
                'note': reward_create.recipient_note
            }
        })
        return {
            'reward_info': response.json()
        }





    @staticmethod
    async def to_reward_db_model(reward_create: RewardCreate):
        return RewardModelDB(
            **reward_create.dict()
        )

    # ver. 1b create_reward, adds reward to db, fetches users from rails and updates reward in db.
    # @classmethod
    # async def create_reward(cls, reward_create: RewardCreate):
    #     rails_api = os.environ["RAILS_API"]
    #     db_model_reward = await cls.to_reward_db_model(reward_create)
    #     reward = await BaseCRUD.create(db_model_reward)
    #     rails_response = requests.get(f"{rails_api}/accounts?company={reward_create.company_id}").json()
    #     if reward and not rails_response:
    #         return {"message":"Reward created, error fetching user from rails."}
    #     user_list = [RewardUser(**user) for user in rails_response['users']]
    #     updated_reward = await cls.update_reward(reward.company_id, reward.uuid, RewardUsersUpdate(company_id=reward.company_id, users=user_list))
    #     if not updated_reward:
    #         return {"message": "Reward created, error updating reward with users from rails."}
    #     return updated_reward

    
    @classmethod
    async def get_rewards_by_company(cls, company_id):
        return await BaseCRUD.get_all_where(
            RewardModelDB,
            [
                RewardModelDB.company_id == company_id
            ]
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
    async def update_reward(cls, company_id, reward_uuid, reward_update):
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
