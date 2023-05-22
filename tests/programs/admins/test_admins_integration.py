import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.programs.program_admin_router import router as admins_router

app = FastAPI()
app.include_router(admins_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_admin():
	client_uuid = "test_client_uuid"
	programs_uuid = "test_programs_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{programs_uuid}/admins")
		assert response.status_code == 200
		assert response.json() == {"message": "Created admin"}

@pytest.mark.asyncio
async def test_integration_get_admins():
	client_uuid = "test_client_uuid"
	programs_uuid = "test_programs_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{programs_uuid}/admins")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all admins"}

@pytest.mark.asyncio
async def test_integration_get_admin():
	client_uuid = "test_client_uuid"
	programs_uuid = "test_programs_uuid"
	admins_uuid = "test_admins_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{programs_uuid}/admins/{admins_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got admins for {admins_uuid}"}

@pytest.mark.asyncio
async def test_integration_update_admin():
	client_uuid = "test_client_uuid"
	programs_uuid = "test_programs_uuid"
	admins_uuid = "test_admins_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{programs_uuid}/admins/{admins_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated admin for {admins_uuid}"}

@pytest.mark.asyncio
async def test_integration_delete_admin():
	client_uuid = "test_client_uuid"
	programs_uuid = "test_programs_uuid"
	admins_uuid = "test_admins_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"clients/{client_uuid}/programs/{programs_uuid}/admins/{admins_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted admin for {admins_uuid}"}
