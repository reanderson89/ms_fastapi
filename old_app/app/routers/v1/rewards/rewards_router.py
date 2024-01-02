from typing import Annotated, List
from fastapi import APIRouter, Path, Body, Depends
from app.models.reward.reward_models import RewardCreate, RewardResponse, RewardUpdate, RewardDelete
from app.actions.rewards.reward_actions import RewardActions
from burp.utils.auth_utils import Permissions


router = APIRouter(tags=["Rewards"])


@router.get("/rewards/{company_id}", response_model=List[RewardResponse])
async def get_rewards_by_company(
    company_id: int = Path(...)
):
    return await RewardActions.get_rewards_by_company(company_id)


@router.get("/rewards/{company_id}/{reward_uuid}", response_model=RewardResponse|None)
async def get_reward(
    company_id: int = Path(...),
    reward_uuid: str = Path(...)
):
    return await RewardActions.get_reward(company_id, reward_uuid)


@router.post("/rewards", response_model=RewardResponse)
async def create_reward(
    jwt: Annotated[str, Depends(Permissions(level="rails"))],
    # request: Request,
    reward_create: RewardCreate = Body(...)
):
    return await RewardActions.create_reward(reward_create)


@router.put("/rewards/{company_id}/{reward_uuid}", response_model=RewardResponse|None)
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
