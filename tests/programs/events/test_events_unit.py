from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.events.router import router as events_router

app = FastAPI()
app.include_router(events_router)
client = TestClient(app)


def test_get_events():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_7char}/events")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all events"}

def test_get_event():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	event_7char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_7char}/events/{event_7char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got events for {event_7char}"}

def test_create_event():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_7char}/events")
	assert response.status_code == 200
	assert response.json() == {"message": "Created event"}

def test_update_event():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	event_7char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_7char}/events/{event_7char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated event for {event_7char}"}
