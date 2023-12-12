from fastapi import APIRouter, Path, Body, Request
from app.models.reward.reward_models import RewardCreate, RewardResponse, RewardUpdate, RewardDelete
from app.actions.rewards.reward_actions import RewardActions
from app.routers.v1.pagination import Page


router = APIRouter(tags=["Rewards"])


@router.get("/rewards/{company_id}", response_model=Page[RewardResponse])
async def get_rewards_by_company(
    company_id: int = Path(...)
):
    return await RewardActions.get_rewards_by_company(company_id)


@router.get("/rewards/{company_id}/{reward_uuid}", response_model=RewardResponse)
async def get_reward(
    company_id: int = Path(...),
    reward_uuid: str = Path(...)
):
    return await RewardActions.get_reward(company_id, reward_uuid)


@router.post("/rewards", response_model=RewardResponse)
async def create_reward(
    request: Request,
    reward_create: RewardCreate = Body(...)
):
    return await RewardActions.create_reward(request, reward_create)


@router.put("/rewards/{company_id}/{reward_uuid}", response_model=RewardResponse)
async def update_reward(
    company_id: int = Path(...),
    reward_uuid: str = Path(...),
    reward_update: RewardUpdate = Body(...)
):
    return await RewardActions.update_reward(company_id, reward_uuid, reward_update)


@router.delete("/rewards/{company_id}/{reward_uuid}", response_model=RewardDelete)
async def delete_reward(
    company_id: int = Path(...),
    reward_uuid: str = Path(...)
):
    return await RewardActions.delete_reward(company_id, reward_uuid)
