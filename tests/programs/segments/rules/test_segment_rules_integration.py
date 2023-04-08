import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.segments.rules.router import router as rules_router

app = FastAPI()
app.include_router(rules_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_rule():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules")
		assert response.status_code == 200
		assert response.json() == {"message": "Created rule"}

@pytest.mark.asyncio
async def test_integration_get_rules():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all rules"}

@pytest.mark.asyncio
async def test_integration_get_rule():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	rule_uuid = "test_rule_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got rules for {rule_uuid}"}

@pytest.mark.asyncio
async def test_integration_update_rule():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	rule_uuid = "test_rule_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated rule for {rule_uuid}"}

@pytest.mark.asyncio
async def test_integration_delete_rule():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	rule_uuid = "test_rule_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted rule for {rule_uuid}"}
