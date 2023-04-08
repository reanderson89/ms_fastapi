from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.segments.awards.router import router as awards_router

app = FastAPI()
app.include_router(awards_router)
client = TestClient(app)


def test_get_awards():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all awards"}

def test_get_award():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	award_uuid = "test_award_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got awards for {award_uuid}"}

def test_create_award():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	response = client.post(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards")
	assert response.status_code == 200
	assert response.json() == {"message": "Created award"}

def test_update_award():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	segment_uuid = 'test_segment_uuid'
	award_uuid = 'test_award_uuid'
	response = client.put(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated award for {award_uuid}"}

def test_delete_award():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	segment_uuid = 'test_segment_uuid'
	award_uuid = 'test_award_uuid'
	response = client.delete(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted award for {award_uuid}"}
