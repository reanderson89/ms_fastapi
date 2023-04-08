import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.segments.awards.router import router as awards_router

app = FastAPI()
app.include_router(awards_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_award():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards")
		assert response.status_code == 200
		assert response.json() == {"message": "Created award"}

@pytest.mark.asyncio
async def test_integration_get_awards():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all awards"}

@pytest.mark.asyncio
async def test_integration_get_award():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	award_uuid = "test_award_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got awards for {award_uuid}"}

@pytest.mark.asyncio
async def test_integration_update_award():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	award_uuid = "test_award_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated award for {award_uuid}"}

@pytest.mark.asyncio
async def test_integration_delete_award():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	award_uuid = "test_award_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted award for {award_uuid}"}
