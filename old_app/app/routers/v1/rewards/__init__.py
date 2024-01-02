from .rewards_router import router as rewards_router
from fastapi import APIRouter

v1_rewards_router = APIRouter()
v1_rewards_router.include_router(rewards_router)
