from fastapi import APIRouter
from app.models.reward.reward_models import RewardCreate, RewardResponse
from app.actions.rewards.reward_actions import RewardActions


router = APIRouter(tags=["Rewards"])


@router.post("/rewards", response_model=RewardResponse)
async def create_reward(reward_create: RewardCreate):
    return await RewardActions.create_reward(reward_create)
