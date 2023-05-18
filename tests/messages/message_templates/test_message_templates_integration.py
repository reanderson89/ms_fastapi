
def test_integration_create_msg_template(test_app):
	response = test_app.post("/messages")
	assert response.status_code == 200
	assert response.json() == {"message": "Created message"}
def test_integration_get_msg_templates(test_app):
	response = test_app.get("/messages")
	assert response.status_code == 200
	assert response.json() == {"message": "Got all messages"}
def test_integration_get_msg_template(test_app):
	message_template_uuid = "test_message_template_uuid"
	response = test_app.get(f"/messages/{message_template_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Got messages for {message_template_uuid}"}
def test_integration_update_msg_template(test_app):
	message_template_uuid = "test_message_template_uuid"
	response = test_app.put(f"/messages/{message_template_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Updated message for {message_template_uuid}"}
def test_integration_delete_msg_template(test_app):
	message_template_uuid = "test_message_template_uuid"
	response = test_app.delete(f"/messages/{message_template_uuid}")
	assert response.status_code == 200
	assert response.json() == {"message": f"Deleted message for {message_template_uuid}"}
