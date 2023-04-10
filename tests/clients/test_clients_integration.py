import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.clients.router import router as clients_router

app = FastAPI()
app.include_router(clients_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_client():
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post("/clients")
		assert response.status_code == 200
		assert response.json() == {"message": "Created client"}

@pytest.mark.asyncio
async def test_integration_get_clients():
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/clients")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all clients"}

@pytest.mark.asyncio
async def test_integration_get_client():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/clients/{client_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got clients for {client_uuid}"}

@pytest.mark.asyncio
async def test_integration_update_client():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"/clients/{client_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated client for {client_uuid}"}
