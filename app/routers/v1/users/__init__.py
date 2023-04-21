from .users_routers import router as users_router
from fastapi import APIRouter

v1_users_router = APIRouter()
v1_users_router.include_router(users_router)
