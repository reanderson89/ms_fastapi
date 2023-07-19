from app.utilities import SHA224Hash

user_uuid = SHA224Hash()
first_client_uuid = SHA224Hash()
second_client_uuid = SHA224Hash()
client_user_uuid = SHA224Hash()


new_user = {
    "uuid": user_uuid,
    "client_uuid": first_client_uuid,
	"first_name": "Test",
	"last_name": "User",
	"primary_work_email": "test.user123@testclient.com",
	"hire_date": "1/1/2015",
	"continuous_service_date": "1/1/2015",
	"employee_id": 1139,
	"manager_id": 200405,
	"cost_center_id": 21121,
	"worker_type": "Employee",
	"department": "Engineering",
	"manager": "Jason W",
	"location": "Seattle",
	"business_title": "Blueboard Engineer",
	"department_leader": 200405
}

new_service = {
	"service_uuid": "email",
	"service_user_id": "test.user2@testclient.com"
}

update_service = {
	"service_user_screenname": "test",
	"service_user_name": "test",
	"service_access_token": "test",
	"service_access_secret": "test",
	"service_refresh_token": "test",
	# "service_uuid": "test"
}

single_client = {
    "uuid":first_client_uuid,
	"name": "test",
	"description": "test",
    "status": 0
}

list_of_clients = [
	{
    "uuid": first_client_uuid,
	"name": "client one",
	"description": "first client",
    "status": 0
	},
	{
    "uuid": second_client_uuid,
	"name": "client two",
	"description": "second client",
    "status": 0
	}
]
new_client_user = {
  "uuid": client_user_uuid,
  "client_uuid": first_client_uuid,
  "email_address": "test.user123@testclient.com",
  "first_name": "Test",
  "last_name": "User",
  "admin": 1
}

update_client_user = {
  "title": "test",
  "department": "test"
} 

new_message = {
	"channel": 0,
	"body": "string",
}

new_program = {
    "user_uuid": None,
    "name": "Blueboard 2023 Anniversary Program",
    "description": "This program sends rewards to Blueboard employees on the Anniversary of their start date at the Company.",
    "budget_9char": "budg_9cha",
    "status": 1,
    "program_type": 4,
    "cadence": 1,
    "cadence_value": 2
  }


