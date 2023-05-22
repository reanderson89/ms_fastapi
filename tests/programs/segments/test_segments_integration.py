import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.segments.segment_router import router as segments_router

app = FastAPI()
app.include_router(segments_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/segments")
		assert response.status_code == 200
		assert response.json() == {"message": "Created segment"}

@pytest.mark.asyncio
async def test_integration_get_segments():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/segments")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all segments"}

@pytest.mark.asyncio
async def test_integration_get_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got segments for {segment_9char}"}

@pytest.mark.asyncio
async def test_integration_update_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated segment for {segment_9char}"}

@pytest.mark.asyncio
async def test_integration_delete_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted segment for {segment_9char}"}
