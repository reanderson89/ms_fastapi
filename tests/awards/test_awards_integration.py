from tests.testutil import new_award, update_award, new_award


def test_integration_get_awards(test_app, award):
	response = test_app.get(f"/v1/awards")
	assert response.status_code == 200
	all_awards = response.json()["items"]
	for award_to_check in all_awards:
		test_award = award_to_check if award_to_check["uuid"] == award["uuid"] else None
	assert test_award["uuid"] == award["uuid"]
	assert test_award["description"] == award["description"]
	assert test_award["name"] == award["name"]


def test_integration_get_award(test_app, award):
	response = test_app.get(f"/v1/awards/{award['uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert response["description"] == award["description"]
	assert response["name"] == award["name"]
	assert response["uuid"] == award["uuid"]


def test_integration_create_award(award):
	assert award["uuid"] == new_award['uuid']
	assert award["description"] == award["description"]
	assert award["name"] == award["name"]


def test_integration_update_award(test_app, award):
	response = test_app.put(f"/v1/awards/{award['uuid']}", json=update_award)
	assert response.status_code == 200
	response = response.json()
	assert response["uuid"] == new_award['uuid']
	assert response["name"] == update_award["name"]
	assert response["description"] == update_award["description"]
	


def test_integration_delete_award(test_app, award):
	response = test_app.delete(f"/v1/awards/{award['uuid']}")
	assert response.status_code == 200
	response = response.json()
	assert response["ok"] == True
	assert response["Deleted"]["uuid"] == award["uuid"]
