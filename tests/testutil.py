from app.utilities import SHA224Hash

user_uuid = SHA224Hash()
first_client_uuid = SHA224Hash()
second_client_uuid = SHA224Hash()
client_user_uuid = SHA224Hash()
program_uuid = SHA224Hash()
award_uuid = SHA224Hash()


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
    "uuid": program_uuid,
    "user_uuid": None,
    "name": "Blueboard 2023 Anniversary Program",
    "description": "This program sends rewards to Blueboard employees on the Anniversary of their start date at the Company.",
    "budget_9char": "budg_9cha",
    "status": 1,
    "program_type": 4,
    "cadence": 1,
    "cadence_value": 2
  }

new_program_admin = {
    "program_uuid": program_uuid,
    "user_uuid": None,
    "permissions": 2
}

update_program_admin = {
    "permissions": 1
}

new_program_event = {
    "event_type": 1,
    "parent_9char": None,
	"event_data": "pytest-event",
	"status": 1
}

update_program_event = {
    "event_type": 2,
    "event_data": "pytest-updated-event",
    "status": 2
}

new_program_segment = {
    "budget_9char": None,
    "name": "pytest segment",
    "description": "this is a segment",
    "status": 1
}

new_award = {
    "uuid": award_uuid,
	"name": "pytest Award",
	"description": "Just a pytest award",
	"channel": 5,
	"award_type": 2,
	"value": 5000
}

update_award = {
	"name": "pytest Award UPDATE",
	"description": "Just a pytest award UPDATE",
	"channel": 4,
	"award_type": 1,
	"value": 10000
}
    
new_client_award = {
	"award_uuid": award_uuid,
	"name": "pytest Client Award",
	"description": "Just a pytest client award",
	"hero_image": None
}

update_client_award = {
    "name": "pytest Client Award UPDATE",
	"description": "Just a pytest client award UPDATE",
	"hero_image": None
}

new_program_award = {
	"name": "pytest Program Award",
	"description": "Just a pytest program award",
    "hero_image": None
}

update_program_award = {
    "name": "pytest Program Award UPDATE",
	"description": "Just a pytest program award UPDATE",
    "hero_image": None
}

new_segment_award = {
    "client_award_9char": None,
    "name": "pytest Segment Award Test",
    "description": "Just a pytest segment award",
    "hero_image": None
}

update_segment_award = {
    "name": "pytest Segment Award Test UPDATE",
    "description": "Just a pytest segment award UPDATE",
    "hero_image": None
}



