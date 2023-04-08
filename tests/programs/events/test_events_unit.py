from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.events.router import router as events_router

app = FastAPI()
app.include_router(events_router)
client = TestClient(app)


def test_get_events():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/events")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all events"}

def test_get_event():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	event_uuid = "test_event_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/events/{event_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got events for {event_uuid}"}

def test_create_event():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	response = client.post(f"/clients/{client_uuid}/programs/{program_uuid}/events")
	assert response.status_code == 200
	assert response.json() == {"message": "Created event"}

def test_update_event():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	event_uuid = 'test_event_uuid'
	response = client.put(f"/clients/{client_uuid}/programs/{program_uuid}/events/{event_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated event for {event_uuid}"}
