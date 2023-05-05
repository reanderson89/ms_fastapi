from .messages_router import router as messages_router
from .message_templates_router import router as templates_router
from fastapi import APIRouter

v1_messages_router = APIRouter()

v1_messages_router.include_router(messages_router)
v1_messages_router.include_router(templates_router)
