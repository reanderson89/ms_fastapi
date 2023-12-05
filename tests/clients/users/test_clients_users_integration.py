from tests.testutil import (
    update_client_user,
    new_client_user_with_user_uuid,
    new_client_user_with_service,
)


def test_integration_create_client_user_with_user_uuid_existing_user(client_user):
    assert "uuid" in client_user
    assert client_user['user_uuid'] == new_client_user_with_user_uuid['user_uuid']
    assert "client_uuid" in client_user


def test_integration_create_client_user_with_user_uuid(test_app, client_user):
    try:
        client_user_2 = test_app.post(f"/v1/clients/{client_user['client_uuid']}/users", json=new_client_user_with_user_uuid)
        assert client_user_2.status_code == 200
        client_user_2 = client_user_2.json()
        assert "uuid" in client_user_2
        assert client_user_2['user_uuid'] == new_client_user_with_user_uuid['user_uuid']
        assert "client_uuid" in client_user_2
    finally:
        test_app.delete(f"/v1/clients/{client_user_2['client_uuid']}/users/{client_user_2['uuid']}")


def test_integration_create_client_user_with_service_exisiting_user(client_user_with_service):
    assert "uuid" in client_user_with_service
    assert "user_uuid" in client_user_with_service
    assert "client_uuid" in client_user_with_service


def test_integration_create_client_user_with_service(test_app, client_user_with_service):
    try:
        client_user = test_app.post(f"/v1/clients/{client_user_with_service['client_uuid']}/users", json=new_client_user_with_service)
        assert client_user.status_code == 200
        client_user = client_user.json()
        assert "uuid" in client_user
        assert "user_uuid" in client_user
        assert "client_uuid" in client_user
    finally:
        test_app.delete(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['uuid']}")


def test_integration_create_client_user_fail(test_app, client):
    client_user = test_app.post(f"/v1/clients/{client['uuid']}/users", json={"first_name": "Should", "last_name": "Fail"})
    assert client_user.status_code == 500
    assert client_user.json()['details']['error']['error_type'] == 'ValueError: No user or client user objects returned'


def test_integration_get_client_users(test_app, client_user):
    response = test_app.get(f"/v1/clients/{client_user['client_uuid']}/users")
    assert response.status_code == 200
    for item in response.json()['items']:
        assert item['client_uuid'] == client_user['client_uuid']
        if item['uuid'] == client_user['uuid']:
            assert True


def test_integration_get_client_user(test_app, client_user):
    response = test_app.get(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['uuid']}")
    assert response.status_code == 200
    response = response.json()
    assert "uuid" in response
    assert response["client_uuid"] == client_user["client_uuid"]
    assert response["user_uuid"] == client_user["user_uuid"]


def test_integration_update_client_user(test_app, client_user):
    response = test_app.put(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['uuid']}", json=update_client_user)
    assert response.status_code == 200
    response = response.json()
    assert response["client_uuid"] == client_user["client_uuid"]
    assert response["uuid"] == client_user["uuid"]
    assert response["title"] == update_client_user["title"]
    assert response["department"] == update_client_user["department"]


def test_integration_delete_client_user(test_app, client_user):
    try:
        assert client_user["client_uuid"] == client_user["client_uuid"]
        response = test_app.delete(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['uuid']}")
        assert response.status_code == 200
        response = response.json()
        assert response["ok"] == True
        assert response["Deleted"]["uuid"] == client_user["uuid"]
    finally:
        test_app.delete(f"/v1/clients/{client_user['client_uuid']}/users/{client_user['uuid']}")
