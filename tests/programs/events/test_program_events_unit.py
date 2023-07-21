from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.programs.program_event_router import router as events_router

app = FastAPI()
app.include_router(events_router)
client = TestClient(app)


def test_get_events():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/events")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all events"}

def test_get_event():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	event_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/events/{event_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got events for {event_9char}"}

def test_create_event():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_9char}/events")
	assert response.status_code == 200
	assert response.json() == {"message": "Created event"}

def test_update_event():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	event_9char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_9char}/events/{event_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated event for {event_9char}"}
