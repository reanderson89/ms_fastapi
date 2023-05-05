from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.clients.client_budgets_router import router as budgets_router

app = FastAPI()
app.include_router(budgets_router)
client = TestClient(app)


def test_get_budgets():
	client_uuid = "test_client_uuid"
	response = client.get(f"/clients/{client_uuid}/budgets")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all budgets"}

def test_get_budget():
	client_uuid = "test_client_uuid"
	budget_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/budgets/{budget_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got budgets for {budget_9char}"}

def test_create_budget():
	client_uuid = "test_client_uuid"
	response = client.post(f"/clients/{client_uuid}/budgets")
	assert response.status_code == 200
	assert response.json() == {"message": "Created budget"}

def test_update_budget():
	client_uuid = "test_client_uuid"
	budget_9char = "testchr"
	response = client.put(f"/clients/{client_uuid}/budgets/{budget_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated budget for {budget_9char}"}

def test_delete_budget():
	client_uuid = "test_client_uuid"
	budget_9char = "testchr"
	response = client.delete(f"/clients/{client_uuid}/budgets/{budget_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted budget for {budget_9char}"}
