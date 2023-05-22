from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.segments.segment_router import router as segments_router

app = FastAPI()
app.include_router(segments_router)
client = TestClient(app)


def test_get_segments():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/segments")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all segments"}

def test_get_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got segments for {segment_9char}"}

def test_create_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_9char}/segments")
	assert response.status_code == 200
	assert response.json() == {"message": "Created segment"}

def test_update_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated segment for {segment_9char}"}

def test_delete_segment():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.delete(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted segment for {segment_9char}"}
