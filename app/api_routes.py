import os
from fastapi import APIRouter, Depends
from burp.utils.auth_utils import get_token, UnAuthedMessage
from starlette import status
from app.routers.v1.cron.cron_router import router as cron_router
from app.routers.v1.rewards.rewards_router import router as rewards_router



ENV: str = os.environ.get("ENV", "local")
JWT_ENFORCED: str = os.environ.get("JWT_ENFORCED", "False").lower()

if JWT_ENFORCED == "false":
    api_router = APIRouter()
else:
    api_router = APIRouter(
            dependencies=[Depends(get_token)],
            responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnAuthedMessage)}
        )


cron_routers = APIRouter()
cron_routers.include_router(cron_router)

api_router.include_router(cron_router, tags=["Cron"])
api_router.include_router(rewards_router, tags=["Rewards"])


@api_router.get("/health", status_code=418)
async def read_root():
    return {"message": "milestones is up and brewing tea"}