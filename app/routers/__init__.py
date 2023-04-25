from fastapi import APIRouter, Depends
from app.utilities.auth import get_token, UnAuthedMessage
from starlette import status
from .v1 import v1router

routers = APIRouter(
        dependencies=[Depends(get_token)],
        responses={status.HTTP_401_UNAUTHORIZED: dict(model=UnAuthedMessage)}
    )

routers.include_router(v1router)
