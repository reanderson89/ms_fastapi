from fastapi import APIRouter
from .segments_router import router as segment_router
from .segments_awards_router import router as awards_router
from .segments_design_router import router as design_router
from .segments_rules_router import router as rules_router

v1_segments_router = APIRouter()
v1_segments_router.include_router(segment_router)
v1_segments_router.include_router(awards_router)
v1_segments_router.include_router(design_router)
v1_segments_router.include_router(rules_router)
