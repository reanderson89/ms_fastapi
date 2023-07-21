from tests.testutil import new_program_event, update_program_event


def test_integration_get_program_events(test_app, program_event):
	response = test_app.get(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events")
	assert response.status_code == 200
	response = response.json()["items"][0]
	assert len(response["event_9char"]) == 9


def test_integration_get_program_event(test_app, program_event):
	response = test_app.get(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events/{program_event['event_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["event_9char"] == program_event["event_9char"]


def test_integration_create_program_event(program_event):
	assert "event_9char" in program_event
	assert program_event["event_data"] == new_program_event["event_data"]


def test_integration_update_program_event(test_app, program_event):
	response = test_app.put(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events/{program_event['event_9char']}", json=update_program_event)
	assert response.status_code == 200
	response = response.json()
	assert response["event_9char"] == program_event["event_9char"]
	assert response["event_type"] == update_program_event["event_type"]
	assert response["event_data"] == update_program_event["event_data"]
	assert response["status"] == update_program_event["status"]


def test_integration_delete_program_event(test_app, program_event):
	response = test_app.delete(f"/v1/clients/{program_event['client_uuid']}/programs/{program_event['program_9char']}/events/{program_event['event_9char']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["event_9char"] == program_event["event_9char"]
	assert response["Deleted"]["client_uuid"] == program_event["client_uuid"]

def test_integration_create_sub_event(sub_event, program_event):
	assert sub_event["parent_9char"] == program_event["event_9char"]
	assert len(sub_event["event_9char"]) == 9