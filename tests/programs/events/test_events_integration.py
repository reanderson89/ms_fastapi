import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.programs.program_events_router import router as events_router

app = FastAPI()
app.include_router(events_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_get_events():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/events")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all events"}

@pytest.mark.asyncio
async def test_integration_get_event():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	event_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/events/{event_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got events for {event_9char}"}

@pytest.mark.asyncio
async def test_integration_create_event():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/events")
		assert response.status_code == 200
		assert response.json() == {"message": "Created event"}

@pytest.mark.asyncio
async def test_integration_update_event():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	event_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{program_9char}/events/{event_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated event for {event_9char}"}
