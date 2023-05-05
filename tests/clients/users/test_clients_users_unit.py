from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.clients.client_users_router import router as users_router

app = FastAPI()
app.include_router(users_router)
client = TestClient(app)


def test_get_users():
	client_uuid = "test_client_uuid"
	response = client.get(f"/clients/{client_uuid}/users")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all users"}

def test_get_user():
	client_uuid = "test_client_uuid"
	user_uuid = 'test_user_uuid'
	response = client.get(f"/clients/{client_uuid}/users/{user_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got users for {user_uuid}"}

def test_create_user():
	client_uuid = "test_client_uuid"
	response = client.post(f"/clients/{client_uuid}/users")
	assert response.status_code == 200
	assert response.json() == {"message": "Created user"}

def test_update_user():
	client_uuid = "test_client_uuid"
	user_uuid = 'test_user_uuid'
	response = client.put(f"/clients/{client_uuid}/users/{user_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated user for {user_uuid}"}

def test_delete_user():
	client_uuid = "test_client_uuid"
	user_uuid = 'test_user_uuid'
	response = client.delete(f"/clients/{client_uuid}/users/{user_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted user for {user_uuid}"}
