from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.clients.client_award_router import router as awards_router

app = FastAPI()
app.include_router(awards_router)
client = TestClient(app)


def test_get_awards():
    client_uuid = "test_client_uuid"
    response = client.get(f"/clients/{client_uuid}/awards")
    assert response.status_code == 200
    assert response.json() == {"message": "Got all awards"}

def test_get_award():
    client_uuid = "test_client_uuid"
    award_9char = "testchr"
    response = client.get(f"/clients/{client_uuid}/awards/{award_9char}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Got awards for {award_9char}"}

def test_create_award():
    client_uuid = "test_client_uuid"
    response = client.post(f"/clients/{client_uuid}/awards")
    assert response.status_code == 200
    assert response.json() == {"message": "Created award"}

def test_update_award():
    client_uuid = "test_client_uuid"
    award_9char = "testchr"
    response = client.put(f"/clients/{client_uuid}/awards/{award_9char}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Updated award for {award_9char}"}

def test_delete_award():
    client_uuid = "test_client_uuid"
    award_9char = "testchr"
    response = client.delete(f"/clients/{client_uuid}/awards/{award_9char}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Deleted award for {award_9char}"}
