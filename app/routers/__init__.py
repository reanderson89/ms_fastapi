from fastapi import APIRouter
from .v1 import v1router

routers = APIRouter()
routers.include_router(v1router)
