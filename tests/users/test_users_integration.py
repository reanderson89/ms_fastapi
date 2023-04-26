import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.users.users_routers import router as users_router

app = FastAPI()
app.include_router(users_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_user():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "Created user"}

@pytest.mark.asyncio
async def test_integration_get_users():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users")
        assert response.status_code == 200
        assert response.json() == {"message": "Got all users"}

@pytest.mark.asyncio
async def test_integration_get_user():
    user_uuid = "test_user_uuid"
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/users/{user_uuid}")
        assert response.status_code == 200
        assert response.json() == {"message": f"Got users for {user_uuid}"}

@pytest.mark.asyncio
async def test_integration_update_user():
    user_uuid = "test_user_uuid"
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/users/{user_uuid}")
        assert response.status_code == 200
        assert response.json() == {"message": f"Updated user for {user_uuid}"}
