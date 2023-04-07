from fastapi import APIRouter
from src.engines.users.router import router as users_router
from src.engines.clients.users.router import router as client_users_router
from src.engines.clients.budgets.router import router as client_budgets_router
from src.engines.clients.awards.router import router as client_awards_router
from src.engines.programs.admins.router import router as program_admins_router
from src.engines.programs.events.router import router as program_events_router
from src.engines.programs.segments.awards.router import router as program_segment_awards_router
from src.engines.programs.segments.rules.router import router as program_segment_rules_router
from src.engines.programs.messages.router import router as program_messages_router
from src.engines.message_templates.router import router as message_templates_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(client_users_router, prefix="/clients/users", tags=["Client Users"])
router.include_router(client_budgets_router, prefix="/clients/budgets", tags=["Client Budgets"])
router.include_router(client_awards_router, prefix="/clients/awards", tags=["Client Awards"])
router.include_router(program_admins_router, prefix="/programs/admins", tags=["Program Admins"])
router.include_router(program_events_router, prefix="/programs/events", tags=["Program Events"])
router.include_router(program_segment_awards_router, prefix="/programs/segments/awards", tags=["Program Segment Awards"])
router.include_router(program_segment_rules_router, prefix="/programs/segments/rules", tags=["Program Segment Rules"])
router.include_router(program_messages_router, prefix="/programs/messages", tags=["Program Messages"])
router.include_router(message_templates_router, prefix="/message-templates", tags=["Message Templates"])
