from app.models.reward.reward_models import RewardCreate
from burp.utils.base_crud import BaseCRUD
from burp.models.reward import RewardModelDB

import os
import requests


class RewardActions:

    # ver. 1a create_reward, does not add reward to db
    @classmethod
    async def create_reward(cls, reward_create: RewardCreate):
        rails_api = os.environ["RAILS_API"]
        url = f'{rails_api}/v4/milestones/rewards'
        r = requests.post(url=url, json=reward_create)
        return r.json()
    
    @staticmethod
    async def to_reward_db_model(reward_create: RewardCreate):
        return RewardModelDB(
            **reward_create.dict()
        )

    # ver. 1b create_reward, adds reward to db
    # @classmethod
    # async def create_reward(cls, reward_create: RewardCreate):
    #     reward_db = await cls.to_reward_db_model(reward_create)
    #     return await BaseCRUD.create(reward_db)
    
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
