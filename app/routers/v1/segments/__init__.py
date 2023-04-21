from fastapi import APIRouter
from .segments_routers import router as segment_router
from .awards import router as awards_router
from .design import router as design_router
from .rules import router as rules_router

v1_segments_router = APIRouter()
v1_segments_router.include_router(segment_router)
v1_segments_router.include_router(awards_router)
v1_segments_router.include_router(design_router)
v1_segments_router.include_router(rules_router)
