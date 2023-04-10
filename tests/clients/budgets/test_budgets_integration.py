import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.clients.budgets.router import router as budgets_router

app = FastAPI()
app.include_router(budgets_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_budget():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"/clients/{client_uuid}/budgets")
		assert response.status_code == 200
		assert response.json() == {"message": "Created budget"}


@pytest.mark.asyncio
async def test_integration_get_budgets():
	client_uuid = "test_client_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/clients/{client_uuid}/budgets")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all budgets"}


@pytest.mark.asyncio
async def test_integration_get_budget():
	client_uuid = "test_client_uuid"
	budget_7char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/clients/{client_uuid}/budgets/{budget_7char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got budgets for {budget_7char}"}


@pytest.mark.asyncio
async def test_integration_update_budget():
	client_uuid = "test_client_uuid"
	budget_7char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"/clients/{client_uuid}/budgets/{budget_7char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated budget for {budget_7char}"}


@pytest.mark.asyncio
async def test_integration_delete_budget():
	client_uuid = "test_client_uuid"
	budget_7char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"/clients/{client_uuid}/budgets/{budget_7char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted budget for {budget_7char}"}
