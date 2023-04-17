from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.router import router as programs_router

app = FastAPI()
app.include_router(programs_router)
client = TestClient(app)


def test_get_programs():
	client_uuid = "test_client_uuid"
	response = client.get(f"/clients/{client_uuid}/programs")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all programs"}

def test_get_program():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got programs for {program_9char}"}

def test_create_program():
	client_uuid = "test_client_uuid"
	response = client.post(f"/clients/{client_uuid}/programs")
	assert response.status_code == 200
	assert response.json() == {"message": "Created program"}

def test_update_program():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated program for {program_9char}"}

def test_delete_program():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.delete(f"/clients/{client_uuid}/programs/{program_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted program for {program_9char}"}
