import os
import pytest
import traceback
from fastapi.testclient import TestClient
from tests.testutil import new_user, single_client, list_of_clients, new_client_user, new_program, new_program_admin, new_program_event, new_award, new_client_award, new_program_award, new_segment_award, new_program_segment

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
		user = test_app.get(f"/v1/users/{client_user['user_uuid']}?expand_services=true")
		user = user.json()
		service_uuid = user["services"]["email"][0]["uuid"]
		yield client_user
	except Exception as e:
		print(f"Exception encountered: {e}")
		traceback.print_exc()
		raise e
	finally:
		if client_user is not None:
			test_app.delete(f"/v1/clients/{client['uuid']}/users/{client_user['uuid']}")
			test_app.delete(f"/v1/users/{user['uuid']}/services/{service_uuid}")
			test_app.delete(f"/v1/users/{user['uuid']}")

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

@pytest.fixture(scope="module")
def program_admin(test_app, program):
	try:
		new_program_admin['user_uuid'] = program['user_uuid']
		program_admin = test_app.post(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/admins", json=new_program_admin)
		program_admin = program_admin.json()
		yield program_admin
	except: 
		raise Exception("Program Admin Creation Failed")
	finally:
		if program_admin is not None:
			test_app.delete(f"/v1/clients/{program_admin['client_uuid']}/programs/{program_admin['program_9char']}/admins/{program_admin['user_uuid']}")

@pytest.fixture(scope="module")
def program_event(test_app, program):
	try:
		program_event = test_app.post(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/events", json=new_program_event)
		program_event = program_event.json()
		yield program_event
	except: 
		raise Exception("Program Event Creation Failed")
	finally:
		if program_event is not None:
			test_app.delete(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events/{program_event['event_9char']}")

@pytest.fixture(scope="module")
def sub_event(test_app, program_event):
	try:
		new_program_event["parent_9char"] = program_event["event_9char"]
		sub_event = test_app.post(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events", json=new_program_event)
		sub_event = sub_event.json()
		yield sub_event
	except: 
		raise Exception("Program Event Creation Failed")
	finally:
		if sub_event is not None:
			test_app.delete(f"/v1/clients/{sub_event['client_uuid']}/programs/{sub_event['program_9char']}/events/{sub_event['event_9char']}")

@pytest.fixture(scope="module")
def segment(test_app, program):
	try:
		program_segment = test_app.post(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/segments", json=new_program_segment)
		program_segment = program_segment.json()
		yield program_segment
	except: 
		raise Exception("Program Segment Creation Failed")
	finally:
		if program_segment is not None:
			test_app.delete(f"/v1/clients/{program_segment['client_uuid']}/programs/{program_segment['program_9char']}/segments/{program_segment['segment_9char']}")

@pytest.fixture(scope="module")
def award(test_app):
	try:
		award = test_app.post(f"/v1/awards", json=new_award)
		award = award.json()
		yield award
	except: 
		raise Exception("Award Creation Failed")
	finally:
		if award is not None:
			test_app.delete(f"/v1/awards/{award['uuid']}")

@pytest.fixture(scope="module")
def client_award(test_app, client):
	try:
		client_award = test_app.post(f"/v1/clients/{client['uuid']}/awards", json=new_client_award)
		client_award = client_award.json()
		yield client_award
	except: 
		raise Exception("Client Award Creation Failed")
	finally:
		if client_award is not None:
			test_app.delete(f"/v1/clients/{client_award['client_uuid']}/awards/{client_award['client_award_9char']}")

@pytest.fixture(scope="module")
def program_award(test_app, program, client_award):
	try:
		program_award = test_app.post(f"/v1/clients/{program['client_uuid']}/programs/{program['program_9char']}/awards/{client_award['client_award_9char']}", json=new_program_award)
		program_award = program_award.json()
		yield program_award
	except: 
		raise Exception("Program Award Creation Failed")
	finally:
		if program_award is not None:
			test_app.delete(f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/awards/{program_award['program_award_9char']}")

@pytest.fixture(scope="module")
def segment_award(test_app, segment, program_award):
	try:
		new_segment_award["client_award_9char"] = program_award["client_award_9char"]
		segment_award = test_app.post(f"/v1/clients/{program_award['client_uuid']}/programs/{program_award['program_9char']}/segments/{segment['segment_9char']}/awards/{program_award['program_award_9char']}", json=new_segment_award)
		segment_award = segment_award.json()
		yield segment_award
	except: 
		raise Exception("Program Award Creation Failed")
	finally:
		if segment_award is not None:
			test_app.delete(f"/v1/clients/{segment_award['client_uuid']}/programs/{segment_award['program_9char']}/segments/{segment_award['segment_9char']}/awards/{segment_award['segment_award_9char']}")


