from .clients_routers import router as client_router
from .awards import router as awards_router
from .budgets import router as budgets_router
from .users import router as users_router
from fastapi import APIRouter

v1_clients_router = APIRouter()
v1_clients_router.include_router(client_router)
v1_clients_router.include_router(awards_router)
v1_clients_router.include_router(budgets_router)
v1_clients_router.include_router(users_router)
