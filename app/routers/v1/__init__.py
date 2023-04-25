from fastapi import APIRouter
from .clients import v1_clients_router
from .programs import v1_program_router
from .messages import v1_messages_router
from .segments import v1_segments_router
from .users import v1_users_router

v1router = APIRouter()

v1router.include_router(v1_users_router)
v1router.include_router(v1_clients_router)
v1router.include_router(v1_program_router)
v1router.include_router(v1_messages_router)
v1router.include_router(v1_segments_router)