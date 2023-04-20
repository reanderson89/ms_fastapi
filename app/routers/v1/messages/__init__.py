from .messages_router import router as messages_router
from .templates import router as templates_router
from fastapi import APIRouter

v1_messages_router = APIRouter()

v1_messages_router.include_router(messages_router, tags=["Messages"])
v1_messages_router.include_router(templates_router, tags=["Templates"])
