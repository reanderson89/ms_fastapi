import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.clients.client_users_router import router as users_router

app = FastAPI()
app.include_router(users_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_user():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post("/clients/{client_uuid}/users")
		assert response.status_code == 200
		assert response.json() == {"message": "Created user"}

@pytest.mark.asyncio
async def test_integration_get_users():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/clients/{client_uuid}/users")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all users"}

@pytest.mark.asyncio
async def test_integration_get_user():
	client_uuid = "test_client_uuid"
	user_id = "test_user_id"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/clients/{client_uuid}/users/{user_id}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got users for {user_id}"}

@pytest.mark.asyncio
async def test_integration_update_user():
	client_uuid = "test_client_uuid"
	user_id = "test_user_id"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"/clients/{client_uuid}/users/{user_id}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated user for {user_id}"}

@pytest.mark.asyncio
async def test_integration_delete_user():
	client_uuid = "test_client_uuid"
	user_id = "test_user_id"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"/clients/{client_uuid}/users/{user_id}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted user for {user_id}"}
