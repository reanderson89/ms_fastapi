import os

from fastapi import APIRouter, Depends
from app.utilities.auth import get_token, UnAuthedMessage
from starlette import status
from .v1 import v1router
from .v1.users.auth.auth_routers import router as auth_router
from .v1.admin.admin_router import router as admin_router


ENV: str = os.environ.get("ENV", "local")

if ENV == "local":
    routers = APIRouter()
else:
    routers = APIRouter(
            dependencies=[Depends(get_token)],
            responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnAuthedMessage)}
        )


auth_routers = APIRouter()

admin_routers = APIRouter(
    dependencies=[Depends(get_token)],
    responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnAuthedMessage)}
)


routers.include_router(v1router)
auth_routers.include_router(auth_router)
admin_routers.include_router(admin_router)
