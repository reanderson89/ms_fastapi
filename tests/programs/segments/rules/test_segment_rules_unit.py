from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.segments.segment_rule_router import router as rules_router

app = FastAPI()
app.include_router(rules_router)
client = TestClient(app)


def test_get_rules():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all rules"}

def test_get_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	rule_9char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got rules for {rule_9char}"}

def test_create_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules")
	assert response.status_code == 200
	assert response.json() == {"message": "Created rule"}

def test_update_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	rule_9char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated rule for {rule_9char}"}

def test_delete_rule():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	segment_9char = "testchr"
	rule_9char = "testchr"
	response = client.delete(f"/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted rule for {rule_9char}"}
