import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.programs.programs_routers import router as programs_router

app = FastAPI()
app.include_router(programs_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_program():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"/clients/{client_uuid}/programs")
		assert response.status_code == 200
		assert response.json() == {"message": "Created program"}

@pytest.mark.asyncio
async def test_integration_get_programs():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/clients/{client_uuid}/programs")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all programs"}

@pytest.mark.asyncio
async def test_integration_get_program():
	client_uuid = "test_client_uuid"
	program_id = "test_program_id"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/clients/{client_uuid}/programs/{program_id}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got programs for {program_id}"}

@pytest.mark.asyncio
async def test_integration_update_program():
	client_uuid = "test_client_uuid"
	program_id = "test_program_id"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"/clients/{client_uuid}/programs/{program_id}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated program for {program_id}"}

@pytest.mark.asyncio
async def test_integration_delete_program():
	client_uuid = "test_client_uuid"
	program_id = "test_program_id"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"/clients/{client_uuid}/programs/{program_id}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted program for {program_id}"}
