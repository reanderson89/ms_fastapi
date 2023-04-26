import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.v1.messages.templates import router as msg_templates_router

app = FastAPI()
app.include_router(msg_templates_router)
client = TestClient(app)


@pytest.mark.asyncio
async def test_integration_create_msg_template():
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.post("/messages")
		assert response.status_code == 200
		assert response.json() == {"message": "Created message"}

@pytest.mark.asyncio
async def test_integration_get_msg_templates():
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get("/messages")
		assert response.status_code == 200
		assert response.json() == {"message": "Got all messages"}

@pytest.mark.asyncio
async def test_integration_get_msg_template():
	message_template_uuid = "test_message_template_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.get(f"/messages/{message_template_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Got messages for {message_template_uuid}"}

@pytest.mark.asyncio
async def test_integration_update_msg_template():
	message_template_uuid = "test_message_template_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.put(f"/messages/{message_template_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Updated message for {message_template_uuid}"}

@pytest.mark.asyncio
async def test_integration_delete_msg_template():
	message_template_uuid = "test_message_template_uuid"
	async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
		response = await ac.delete(f"/messages/{message_template_uuid}")
		assert response.status_code == 200
		assert response.json() == {"message": f"Deleted message for {message_template_uuid}"}
