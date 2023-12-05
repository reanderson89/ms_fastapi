from app.models.reward.reward_models import RewardCreate
import requests
import os


class RewardActions:

    @classmethod
    async def create_reward(cls, reward_create: RewardCreate):
        rails_api = os.environ["RAILS_API"]
        url = f'{rails_api}/rewards/<name_pending>'
        r = requests.post(url=url, json=reward_create)
        return r.json()
