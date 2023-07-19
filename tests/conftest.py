import os
import pytest
import traceback
from fastapi.testclient import TestClient
from tests.testutil import new_user, single_client, list_of_clients, new_client_user, new_program

os.environ["TEST_MODE"] = "True"

from app.main import app


def delete_user(test_app, user):
	response = test_app.delete(f"/v1/delete_test_user/{user['uuid']}/")
	assert response.status_code == 200
	assert response.text == "Test User Deleted"

@pytest.fixture(scope="module")
def test_app():
	client = TestClient(app)
	yield client

@pytest.fixture(scope="module")
def user(test_app):
	try:
		user = test_app.post("/v1/users", json=new_user)
		user = user.json()
		yield user
	except:
		raise Exception("User Creation Failed")
	finally:
		if user is not None:
			delete_user(test_app, user)

@pytest.fixture(scope="module")
def service(test_app, user):
	response = test_app.get(f"/v1/users/{user['uuid']}/services")
	user_service = response.json()['email'][0]
	yield user_service

# FOR TESTING CLIENT ROUTES
@pytest.fixture(scope="module")
def client(test_app):
	try:
		client = test_app.post(f"/v1/clients", json=single_client)
		client = client.json()
		yield client
	except:
		raise Exception("Client Creation Failed")
	finally:
		if client is not None:
			test_app.delete(f"/v1/clients/{client['uuid']}")

@pytest.fixture(scope="module")
def clients(test_app):
	try:
		clients = test_app.post(f"/v1/clients", json=list_of_clients)
		clients = clients.json()
		yield clients
	except:
		raise Exception("Client Creation Failed")
	finally:
		for client in clients:
			if client is not None:
				test_app.delete(f"/v1/clients/{client['uuid']}")


@pytest.fixture(scope="module")
def client_user(test_app, client):
	client_user = None
	try:
		client_user = test_app.post(f"/v1/clients/{client['uuid']}/users", json=new_client_user)
		client_user = client_user.json()
		yield client_user
	except Exception as e:
		print(f"Exception encountered: {e}")
		traceback.print_exc()
		raise e
	finally:
		if client_user is not None:
			test_app.delete(f"/v1/clients/{client['uuid']}/users/{client_user['uuid']}")

@pytest.fixture(scope="module")
def program(test_app, client_user):
	try:
		new_program["user_uuid"] = client_user["user_uuid"]
		program = test_app.post(f"/v1/clients/{client_user['client_uuid']}/programs/", json=new_program)
		program = program.json()[0]
		yield program
	except Exception as e:
		print(f"Exception encountered: {e}")
		traceback.print_exc()
		raise e
	finally:
		if program is not None:
			test_app.delete(f"/v1/clients/{client_user['client_uuid']}/programs/{program['program_9char']}")



# @pytest.fixture(scope="module")
# def test_app_with_db():
# 	test_app = TestClient(app)
# 	app.dependency_overrides[get_db] = override_get_db
# 	yield test_app
# 	app.dependency_overrides.clear()
