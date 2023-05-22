from .program_admin_router import router as admin_router
from .program_event_router import router as event_router
from .program_router import router as program_router
from fastapi import APIRouter

v1_program_router = APIRouter()
v1_program_router.include_router(program_router)
v1_program_router.include_router(admin_router)
v1_program_router.include_router(event_router)
