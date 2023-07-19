from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users import UserActions
from app.models.clients import ClientUserModelDB, ClientUserExpand 
from app.models.users import UserModelDB, UserServiceModelDB
from app.exceptions import ExceptionHandling
from app.utilities import SHA224Hash
from time import time

class ClientUserActions():

	@staticmethod
	async def get_client_user_by_user_uuid(uuid: str):
		return await BaseActions.check_if_exists(
			ClientUserModelDB,
			[
				ClientUserModelDB.user_uuid == uuid
			]
		)
	
	@staticmethod
	async def expand_client_user(client_user, user):
		client_user_expanded = ClientUserExpand.from_orm(client_user)
		client_user_expanded.user = user
		return client_user_expanded

	@classmethod
	async def create_client_user(cls, data: dict, path_params: dict, expand: bool = False):
		service_id = ["work_email", "personal_email", "cell_phone", "email_address"]
		user_objs = []
		client_user_objs = []
		for service in service_id:
			if service in data: #.keys()
				response_obj = await cls.handle_user_and_service(data, path_params, expand, service)
				if isinstance(response_obj, UserModelDB):
					user_objs.append(response_obj)
				elif isinstance(response_obj, ClientUserModelDB) or isinstance(response_obj, ClientUserExpand):
					client_user_objs.append(response_obj)
		if not user_objs and not client_user_objs:
			raise ValueError("No user or client user objects returned")

		user_obj = set([user.uuid for user in user_objs if user is not None])
		if len(user_obj) > 1:
			raise ValueError("Multiple user objects returned for different service IDs")

		client_user_obj = set([user.uuid for user in client_user_objs if user is not None])
		if len(client_user_obj) > 1:
			raise ValueError("Multiple client user objects returned for different service IDs")

		new_client_user = await cls.add_new_client_user(
				data, path_params, user_objs[0]
			) if not client_user_objs else client_user_objs[0]
		return new_client_user

	@classmethod
	async def handle_user_and_service(cls, data: dict, path_params, expand, service_id = None):
		user = None
		if service_id not in data.keys() and "user_uuid" not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User. Please include either email address or the user_uuid.")
		if service_id in data.keys():
			user = await BaseActions.check_if_exists(
				UserModelDB,
				[
					UserServiceModelDB.service_user_id == data.get(service_id),
					UserModelDB.uuid == UserServiceModelDB.user_uuid
				])

		if "user_uuid" in data.keys() or user is not None:
			uuid = user.uuid if user is not None else data["user_uuid"]
			client_user = await cls.get_client_user_by_user_uuid(uuid)
			if client_user and expand:
				return await cls.expand_client_user(client_user, user)
			return client_user

		if not user and service_id in data.keys():
			admin = data.setdefault("admin", 0)
			if admin not in [0,1,2]:
				await ExceptionHandling.custom409("Invalid value for admin field, must be 0 or 1.")
			user = await UserActions.create_user_and_service(data, service_id)

		if not user and service_id not in data.keys() and "user_uuid" not in data.keys():
			return await ExceptionHandling.custom409("Not enough information to create a new Client User, User, and Service User. Please include an email address.")

		return user

	@classmethod
	async def add_new_client_user(cls, data: dict, path_params: dict, user):
		# Check if client user already exists
		client_user = await cls.get_client_user_by_user_uuid(user.uuid)
		
		if not client_user:
			# Create new client user object
			client_user_obj = ClientUserModelDB(
				uuid=SHA224Hash(),
				user_uuid=user.uuid,
				client_uuid=path_params.get("client_uuid"),
				manager_uuid=await HelperActions.get_manager_uuid(data),
				employee_id=await HelperActions.get_employee_id(data),
				title=await HelperActions.get_title(data),
				department=await HelperActions.get_department(data),
				active=await HelperActions.get_active(data) if "active" in data.keys() else 1,
				time_hire=int(time()),
				time_start=int(time()),
				admin=await HelperActions.get_admin(data),
			)

			# Save client user object to database
			client_user = await BaseActions.create(client_user_obj)
		return await cls.expand_client_user(client_user, user)

	@classmethod
	async def getExpandedClientUsers(cls, data, client_uuid, expansion):
		pass

	@staticmethod
	async def get_all_users(client_uuid: str, query_params: dict):
		return await BaseActions.get_all_where(
			ClientUserModelDB,
			[
				ClientUserModelDB.client_uuid == client_uuid
			],
			query_params
		)

	@staticmethod
	async def get_user(path_params):
		return await BaseActions.get_one_where(
			ClientUserModelDB,
			[
				ClientUserModelDB.client_uuid == path_params['client_uuid'],
				ClientUserModelDB.user_uuid == path_params['user_uuid']
			]
		)

	@staticmethod
	async def update_user(path_params: dict, user_updates):
		return await BaseActions.update(
			ClientUserModelDB,
			[
				ClientUserModelDB.client_uuid == path_params['client_uuid'],
				ClientUserModelDB.uuid == path_params['user_uuid']
			],
			user_updates
		)

	@staticmethod
	async def update_users(path_params, user_updates):
		uuid_list = []
		for user in user_updates:
			if user.uuid:
				uuid_list.append(user.uuid)
			else:
				return await ExceptionHandling.custom400(f"Missing uuid in user update list for: {user}")
		return await BaseActions.bulk_update(
			ClientUserModelDB,
			[
				ClientUserModelDB.client_uuid == path_params.get('client_uuid'),
			],
			user_updates,
			uuid_list
		)
	
	@staticmethod
	async def update_admin_client_user(path_params: dict, user_updates):
		if path_params.get("client_uuid") is None:
			conditions = [ClientUserModelDB.user_uuid == path_params['user_uuid']]
		else:
			conditions = [
				ClientUserModelDB.client_uuid == path_params['client_uuid'],
				ClientUserModelDB.user_uuid == path_params['user_uuid']
			]
		
		return await BaseActions.update(
			ClientUserModelDB,
			conditions,
			user_updates
		)

	@staticmethod
	async def delete_user(path_params):
		return await BaseActions.delete_one(
			ClientUserModelDB,
			[
				ClientUserModelDB.client_uuid == path_params['client_uuid'],
				ClientUserModelDB.uuid == path_params['user_uuid']
			]
		)
