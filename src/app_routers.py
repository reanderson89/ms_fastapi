from fastapi import APIRouter
from api.users.users_router import router as users_router
from api.clients.client_router import router as client_router
from src.api.clients.users.router import router as client_users_router
from api.clients.budgets.budget_router import router as client_budgets_router
from src.api.clients.awards.router import router as client_awards_router
from src.api.programs.router import router as program_router
from src.api.programs.admins.router import router as program_admins_router
from src.api.programs.events.router import router as program_events_router
from src.api.programs.segments.router import router as program_segments_router
from api.programs.segments.awards.segment_award_router import router as program_segment_awards_router
from src.api.programs.segments.rules.router import router as program_segment_rules_router
from src.api.programs.messages.router import router as program_messages_router
from src.api.messages.router import router as msg_templates_router

router = APIRouter()
router.include_router(users_router, tags=["Users"])
router.include_router(client_router, prefix="/clients", tags=["Clients"])
router.include_router(client_users_router, tags=["Client Users"])
router.include_router(client_budgets_router, tags=["Client Budgets"])
router.include_router(client_awards_router, tags=["Client Awards"])
router.include_router(program_router, tags=["Programs"])
router.include_router(program_admins_router, tags=["Program Admins"])
router.include_router(program_events_router, tags=["Program Events"])
router.include_router(program_segments_router, tags=["Program Segments"])
router.include_router(program_segment_awards_router, tags=["Program Segment Awards"])
router.include_router(program_segment_rules_router, tags=["Program Segment Rules"])
router.include_router(program_messages_router, tags=["Program Messages"])
router.include_router(msg_templates_router, tags=["Message Templates"])
