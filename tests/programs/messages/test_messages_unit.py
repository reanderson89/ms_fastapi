from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.engines.programs.messages.router import router as messages_router

app = FastAPI()
app.include_router(messages_router)
client = TestClient(app)


def test_get_messages():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_7char}/messages")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all messages"}

def test_get_message():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	message_7char = "testchr"
	response = client.get(f"/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got messages for {message_7char}"}

def test_create_message():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_7char}/messages")
	assert response.status_code == 200
	assert response.json() == {"message": "Created message"}

def test_create_message_from_template():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	message_7char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Created message from template for {message_7char}"}

def test_test_message():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	message_7char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}/test")
	assert response.status_code == 200
	assert response.json() == {"message": f"Tested message for {message_7char}"}

def test_send_message():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	message_7char = "testchr"
	response = client.post(f"/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}/send")
	assert response.status_code == 200
	assert response.json() == {"message": f"Sent message for {message_7char}"}

def test_update_message():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	message_7char = "testchr"
	response = client.put(f"/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated message for {message_7char}"}

def test_delete_message():
	client_uuid = "test_client_uuid"
	program_7char = "testchr"
	message_7char = "testchr"
	response = client.delete(f"/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted message for {message_7char}"}
