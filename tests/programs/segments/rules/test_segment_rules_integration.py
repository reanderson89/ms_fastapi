import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.segments.rules import router as rules_router

app = FastAPI()
app.include_router(rules_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules")
		assert response.status_code == 200
		assert response.json() == {"message": "Created rule"}

@pytest.mark.asyncio
async def test_integration_get_rules():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all rules"}

@pytest.mark.asyncio
async def test_integration_get_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	rule_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got rules for {rule_9char}"}

@pytest.mark.asyncio
async def test_integration_update_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	rule_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated rule for {rule_9char}"}

@pytest.mark.asyncio
async def test_integration_delete_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	rule_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted rule for {rule_9char}"}
