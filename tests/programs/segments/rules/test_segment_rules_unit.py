from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.segments.rules.router import router as rules_router

app = FastAPI()
app.include_router(rules_router)
client = TestClient(app)


def test_get_rules():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all rules"}

def test_get_rule():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	rule_uuid = "test_rule_uuid"
	response = client.get(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got rules for {rule_uuid}"}

def test_create_rule():
	client_uuid = "test_client_uuid"
	program_uuid = "test_program_uuid"
	segment_uuid = "test_segment_uuid"
	response = client.post(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules")
	assert response.status_code == 200
	assert response.json() == {"message": "Created rule"}

def test_update_rule():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	segment_uuid = 'test_segment_uuid'
	rule_uuid = 'test_rule_uuid'
	response = client.put(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated rule for {rule_uuid}"}

def test_delete_rule():
	client_uuid = "test_client_uuid"
	program_uuid = 'test_program_uuid'
	segment_uuid = 'test_segment_uuid'
	rule_uuid = 'test_rule_uuid'
	response = client.delete(f"/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted rule for {rule_uuid}"}
