import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.messages.messages_router import router as messages_router

app = FastAPI()
app.include_router(messages_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_message():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/messages")
		assert response.status_code == 200
		assert response.json() == {"message": "Created message"}

@pytest.mark.asyncio
async def test_integration_get_messages():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/messages")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all messages"}

@pytest.mark.asyncio
async def test_integration_get_message():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	message_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"clients/{client_uuid}/programs/{program_9char}/messages/{message_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got messages for {message_9char}"}

@pytest.mark.asyncio
async def test_integration_create_template_message():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	message_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/messages/{message_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Created message from template for {message_9char}"}

@pytest.mark.asyncio
async def test_integration_test_message():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	message_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/messages/{message_9char}/test")
		assert response.status_code == 200
		assert response.json() == {"message": f"Tested message for {message_9char}"}

@pytest.mark.asyncio
async def test_integration_send_message():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	message_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post(f"clients/{client_uuid}/programs/{program_9char}/messages/{message_9char}/send")
		assert response.status_code == 200
		assert response.json() == {"message": f"Sent message for {message_9char}"}

@pytest.mark.asyncio
async def test_integration_upate_message():
	client_uuid = "test_client_uuid"
	program_9char = "testchr"
	message_9char = "testchr"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"clients/{client_uuid}/programs/{program_9char}/messages/{message_9char}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated message for {message_9char}"}