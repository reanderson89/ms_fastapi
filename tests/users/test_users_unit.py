from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.users.users_routers import router as users_router

app = FastAPI()
app.include_router(users_router)
client = TestClient(app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == {"message": "Got all users"}

def test_get_user():
    user_uuid = "test_user_uuid"
    response = client.get(f"/users/{user_uuid}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Got users for {user_uuid}"}

def test_create_user():
    response = client.post("/users")
    assert response.status_code == 200
    assert response.json() == {"message": "Created user"}

def test_update_user():
    user_uuid = "test_user_uuid"
    response = client.put(f"/users/{user_uuid}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Updated user for {user_uuid}"}
