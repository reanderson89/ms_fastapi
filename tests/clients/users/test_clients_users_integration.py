
# def test_integration_create_user(test_app, client_user):
# 	response = test_app.post(f"/v1/clients/{client_uuid}/users")
# 	assert response.status_code == 200
# 	assert response.json() == {"message": "Created user"}

def test_integration_get_users(test_app, client_user):
	response = test_app.get(f"/v1/clients/{client_user['client_uuid']}/users")
	response = response.json()[0]
	assert response.status_code == 200
	assert response['client_uuid'] == client_user['client_uuid']
	assert response['uuid'] == client_user['uuid']

# def test_integration_get_user(test_app):
# 	client_uuid = "test_client_uuid"
# 	user_id = "test_user_id"
# 	response = test_app.get(f"/clients/{client_uuid}/users/{user_id}")
# 	assert response.status_code == 200
# 	assert response.json() == {"message": f"Got users for {user_id}"}

# def test_integration_update_user(test_app):
# 	client_uuid = "test_client_uuid"
# 	user_id = "test_user_id"
# 	response = test_app.put(f"/clients/{client_uuid}/users/{user_id}")
# 	assert response.status_code == 200
# 	assert response.json() == {"message": f"Updated user for {user_id}"}

# def test_integration_delete_user(test_app):
# 	client_uuid = "test_client_uuid"
# 	user_id = "test_user_id"
# 	response = test_app.delete(f"/clients/{client_uuid}/users/{user_id}")
# 	assert response.status_code == 200
# 	assert response.json() == {"message": f"Deleted user for {user_id}"}
