new_user = {
	"legal_first_name": "Test",
	"legal_last_name": "User",
	"primary_work_email": "test.user1@testclient.com",
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
	"name": "test",
	"description": "test",
}
list_of_clients = [
	{
	"name": "client one",
	"description": "first client",
	},
	{
	"name": "client two",
	"description": "second client",
	}
]
new_client_user = {
	"client_uuid": "string",
	"manager_uuid": "string",
	"employee_id": "string",
	"title": "string",
	"department": "string",
	"active": True,
	"time_hire": 0,
	"time_start": 0,
	"admin": 0
}
new_message = {
	"channel": 0,
	"body": "string",
}
