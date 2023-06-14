from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users import UserActions
from app.models.clients import ClientUserModel
from app.models.users import UserModel, UserServiceModel
from app.exceptions import ExceptionHandling
from app.utilities import SHA224Hash
from time import time

class ClientUserActions():

	@staticmethod
	async def get_client_user_by_user_uuid(uuid: str):
		return await BaseActions.check_if_exists(
			ClientUserModel,
			[
				ClientUserModel.user_uuid == uuid
			]
		)

	@classmethod
	async def create_client_user(cls, data, path_params):
		user = None
		if 'email_address' not in data.keys() and 'user_uuid' not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User. Please inclue either email address or the user_uuid.")

		if 'email_address' in data.keys():
			user = await BaseActions.check_if_exists(
				UserModel,
				[
					UserServiceModel.service_user_id == data['email_address'],
					UserModel.uuid == UserServiceModel.user_uuid
				])

		if 'user_uuid' in data.keys() or user is not None:
			uuid = user.uuid if user is not None else data['user_uuid']
			client_user = await cls.get_client_user_by_user_uuid(uuid)
			if client_user:
				return client_user

		if not user and 'email_address' in data.keys():
			user = await UserActions.create_user_and_service(data)

		if not user and 'email_address' not in data.keys() and 'user_uuid' not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User, User, and Service User. Please include an email address.")
		newClientUser = ClientUserModel(
			uuid=SHA224Hash(),
			user_uuid= user.uuid,
			client_uuid= path_params['client_uuid'],
			manager_uuid= await HelperActions.get_manager_uuid(data),
			employee_id= await HelperActions.get_employee_id(data),
			title= await HelperActions.get_title(data),
			department= await HelperActions.get_department(data),
			active=await HelperActions.get_active(data),
			time_hire=int(time()),
			time_start=int(time()),
			admin= await HelperActions.get_admin(data),
		)
		return await BaseActions.create(newClientUser)

	@classmethod
	async def getExpandedClientUsers(cls, data, client_uuid, expansion):
		pass

	@staticmethod
	async def get_all_users(path_params):
		return await BaseActions.get_all_where(
			ClientUserModel,
			[
				ClientUserModel.client_uuid == path_params['client_uuid']
			]
		)

	@staticmethod
	async def get_user(path_params):
		return await BaseActions.get_one_where(
			ClientUserModel,
			[
				ClientUserModel.client_uuid == path_params['client_uuid'],
				ClientUserModel.user_uuid == path_params['user_uuid']
			]
		)

	@staticmethod
	async def update_user(path_params, user_updates):
		return await BaseActions.update(
			ClientUserModel,
			[
				ClientUserModel.client_uuid == path_params['client_uuid'],
				ClientUserModel.uuid == path_params['user_uuid']
			],
			user_updates
		)

	@staticmethod
	async def delete_user(path_params):
		return await BaseActions.delete_one(
			ClientUserModel,
			[
				ClientUserModel.client_uuid == path_params['client_uuid'],
				ClientUserModel.uuid == path_params['user_uuid']
			]
		)
