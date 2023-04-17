from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.segments.awards.router import router as awards_router

app = FastAPI()
app.include_router(awards_router)
client = TestClient(app)


def test_get_awards():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/awards")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all awards"}

def test_get_award():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	award_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/awards/{award_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got awards for {award_9char}"}

def test_create_award():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/awards")
	assert response.status_code == 200
	assert response.json() == {"message": "Created award"}

def test_update_award():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	award_9char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/awards/{award_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated award for {award_9char}"}

def test_delete_award():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	award_9char = "testchr"
	response = client.delete(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/awards/{award_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted award for {award_9char}"}
