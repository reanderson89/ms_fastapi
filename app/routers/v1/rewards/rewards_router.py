from fastapi import APIRouter, Depends, Path
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.models.reward.reward_models import (
    StagedRewardCountResponse,
    StagedRewardResponse
)


router = APIRouter(tags=["Staged Rewards"])

@router.get("/staged_rewards/{company_id}/count", response_model=StagedRewardCountResponse)
async def get_reward_count_for_rule(
    company_id: int = Path(...)
):
    return await StagedRewardActions.get_reward_count_for_rule(company_id)

@router.get("/staged_rewards/{company_id}", response_model=Page[StagedRewardResponse])
async def get_staged_rewards(
    company_id: int = Path(...),
    query_params: dict = Depends(default_query_params)
):
    return await StagedRewardActions.get_staged_rewards(company_id, query_params)

