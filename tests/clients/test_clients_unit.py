from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.clients.router import router as clients_router

app = FastAPI()
app.include_router(clients_router)
client = TestClient(app)


def test_get_clients():
	response = client.get("/clients")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all clients"}

def test_get_client():
	client_uuid = 1
	response = client.get(f"/clients/{client_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got clients for {client_uuid}"}

def test_create_client():
	response = client.post("/clients")
	assert response.status_code == 200
	assert response.json() == {"message": "Created client"}

def test_update_client():
	client_uuid = 1
	response = client.put(f"/clients/{client_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated client for {client_uuid}"}
