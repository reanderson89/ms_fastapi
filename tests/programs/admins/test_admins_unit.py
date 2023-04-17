from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.admins.router import router as admins_router

app = FastAPI()
app.include_router(admins_router)
client = TestClient(app)


def test_get_admins():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/admins")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all admins"}

def test_get_admin():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	admin_uuid = "test_admin_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/admins/{admin_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got admins for {admin_uuid}"}

def test_create_admin():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_9char}/admins")
	assert response.status_code == 200
	assert response.json() == {"message": "Created admin"}

def test_update_admin():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	admin_uuid = 'test_admin_uuid'
	response = client.put(f"/clients/{client_uuid}/programs/{program_9char}/admins/{admin_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated admin for {admin_uuid}"}

def test_delete_admin():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	admin_uuid = 'test_admin_uuid'
	response = client.delete(f"/clients/{client_uuid}/programs/{program_9char}/admins/{admin_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted admin for {admin_uuid}"}
