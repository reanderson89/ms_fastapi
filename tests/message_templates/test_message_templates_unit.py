from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.messages.router import router as msg_templates_router

app = FastAPI()
app.include_router(msg_templates_router)
client = TestClient(app)


def test_get_msg_templates():
	response = client.get("/messages")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all messages"}

def test_get_msg_template():
	message_template_uuid = "test_message_template_uuid"
	response = client.get(f"/messages/{message_template_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got messages for {message_template_uuid}"}

def test_create_msg_template():
	response = client.post("/messages")
	assert response.status_code == 200
	assert response.json() == {"message": "Created message"}

def test_update_msg_template():
	message_template_uuid = "test_message_template_uuid"
	response = client.put(f"/messages/{message_template_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated message for {message_template_uuid}"}

def test_delete_msg_template():
	message_template_uuid = "test_message_template_uuid"
	response = client.delete(f"/messages/{message_template_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted message for {message_template_uuid}"}
