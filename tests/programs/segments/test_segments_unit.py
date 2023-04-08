from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.segments.router import router as segments_router

app = FastAPI()
app.include_router(segments_router)
client = TestClient(app)


def test_get_segments():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/segments")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all segments"}

def test_get_segment():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got segments for {segment_uuid}"}

def test_create_segment():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	response = client.post(f"/clients/{client_uuid}/programs/{program_uuid}/segments")
	assert response.status_code == 200
	assert response.json() == {"message": "Created segment"}

def test_update_segment():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	segment_uuid = 'test_segment_uuid'
	response = client.put(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated segment for {segment_uuid}"}

def test_delete_segment():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	segment_uuid = 'test_segment_uuid'
	response = client.delete(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted segment for {segment_uuid}"}
