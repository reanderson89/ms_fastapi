import pytest
import httpx
from app.main import app
from tests.testutil import new_service, update_service


@pytest.mark.asyncio
async def test_get_all_users_async():
	async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
		response = await ac.get("/v1/users/")
		assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_all_services_async(test_app, user):
	async with httpx.AsyncClient(app=app, base_url="http://testserver") as ac:
		response = await ac.get(f"/v1/users/{user['uuid']}/services/")
		assert response.status_code == 200
		assert response.json()['email'][0]['user_uuid'] == user['uuid']

def test_get_all_services(test_app, user):
	response = test_app.get(f"/v1/users/{user['uuid']}/services/")
	assert response.status_code == 200
	assert response.json()['email'][0]['user_uuid'] == user['uuid']

def test_get_all_users(test_app):
	response = test_app.get("/v1/users/")
	assert response.status_code == 200

def test_get_service(test_app, service):
	response = test_app.get(f"/v1/users/{service['user_uuid']}/services/{service['uuid']}/")
	assert response.status_code == 200
	assert response.json()['uuid'] == service['uuid']

def test_create_user_service(test_app, user):
	response = test_app.post(f"/v1/users/{user['uuid']}/services/", json=new_service)
	assert response.status_code == 200
	assert response.json()['user_uuid'] == user['uuid']

def test_update_user_service(test_app, service):
	response = test_app.put(f"/v1/users/{service['user_uuid']}/services/{service['uuid']}/", json=update_service)
	assert response.status_code == 200
	assert response.json()['service_user_name'] == update_service['service_user_name']
