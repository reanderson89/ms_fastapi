from .admins import router as admin_router
from .events import router as event_router
from .programs_routers import router as program_router
from fastapi import APIRouter

v1_program_router = APIRouter()
v1_program_router.include_router(admin_router, tags=["Admin"])
v1_program_router.include_router(event_router, tags=["Events"])
v1_program_router.include_router(program_router, tags=["Programs"])