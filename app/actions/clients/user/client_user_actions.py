from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users import UserActions
from app.models.clients import ClientUserModelDB
from app.models.users import UserModel, UserServiceModelDB
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

	@classmethod
	async def create_client_user(cls, data: dict, path_params: dict):
		service_id = ["work_email", "personal_email", "cell_phone"]
		user_objs = []
		client_user_objs = []
		for service in service_id:
			if service in data: #.keys()
				user_or_client_user_objs = await cls.handle_user_and_service(data, path_params, service)
				if isinstance(user_or_client_user_objs, UserModel):
					user_objs.append(user_or_client_user_objs)
				elif isinstance(user_or_client_user_objs, ClientUserModelDB):
					client_user_objs.append(user_or_client_user_objs)

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
	async def handle_user_and_service(cls, data, path_params, service_id = None):
		user = None

		if service_id not in data.keys() and "user_uuid" not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User. Please include either email address or the user_uuid.")

		if service_id in data.keys():
			user = await BaseActions.check_if_exists(
				UserModel,
				[
					UserServiceModelDB.service_user_id == service_id,
					UserModel.uuid == UserServiceModelDB.user_uuid
				])

		if "user_uuid" in data.keys() or user is not None:
			uuid = user.uuid if user is not None else data["user_uuid"]
			client_user = await cls.get_client_user_by_user_uuid(uuid)
			if client_user:
				return client_user

		if not user and service_id in data.keys():
			admin = data.setdefault("admin", 0)
			if admin not in [0,1]:
				await ExceptionHandling.custom400("Invalid value for admin field, must be 0 or 1.")
			user = await UserActions.create_user_and_service(data, service_id)

		if not user and service_id not in data.keys() and "user_uuid" not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User, User, and Service User. Please include an email address.")

		return user

	@classmethod
	async def add_new_client_user(cls, data, path_params, user = None):
		client_user_obj = ClientUserModelDB(
			uuid=SHA224Hash(),
			user_uuid= user.uuid,
			client_uuid= path_params["client_uuid"],
			manager_uuid= await HelperActions.get_manager_uuid(data),
			employee_id= await HelperActions.get_employee_id(data),
			title= await HelperActions.get_title(data),
			department= await HelperActions.get_department(data),
			active=await HelperActions.get_active(data),
			time_hire=int(time()),
			time_start=int(time()),
			admin= await HelperActions.get_admin(data),
		)
		return await BaseActions.create(client_user_obj)

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
	async def update_user(path_params, user_updates):
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
	async def delete_user(path_params):
		return await BaseActions.delete_one(
			ClientUserModelDB,
			[
				ClientUserModelDB.client_uuid == path_params['client_uuid'],
				ClientUserModelDB.uuid == path_params['user_uuid']
			]
		)
