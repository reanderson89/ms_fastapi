from .clients_routers import router as client_router
from .awards import router as awards_router
from .budgets import router as budgets_router
from .users import router as users_router
from fastapi import APIRouter

v1_clients_router = APIRouter()
v1_clients_router.include_router(client_router, tags=["Clients"])
v1_clients_router.include_router(awards_router, tags=["Awards"])
v1_clients_router.include_router(budgets_router, tags=["Budget"])
v1_clients_router.include_router(users_router, tags=["Users"])
