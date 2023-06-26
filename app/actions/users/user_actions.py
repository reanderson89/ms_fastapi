from time import time
from datetime import datetime
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users.services import UserServiceActions
from app.models.users import UserModel, UserServiceModelDB, UserExpanded

class UserActions(BaseActions):

	@staticmethod
	def getTimeFromBday(bday):
		date_obj = datetime.strptime(bday, "%m/%d/%Y")
		epoch_time = int(date_obj.timestamp())
		return epoch_time

	@classmethod
	async def get_user_by_uuid(cls, uuid):
		return await cls.get_one_where(UserModel, [UserModel.uuid == uuid])

	@classmethod
	async def get_user_by_service_id(cls, service_id):
		return await cls.check_if_exists(
			UserModel,
			[
			UserServiceModelDB.service_user_id == service_id,
			UserServiceModelDB.user_uuid == UserModel.uuid
			]
		)

	@classmethod
	async def get_all_users(cls, query_params: dict):
		return await cls.get_all(UserModel, query_params)

	@classmethod
	async def get_user(cls, user_uuid, expand_services=False):
		user = await cls.get_user_by_uuid(user_uuid)
		if expand_services:
			user_expanded = UserExpanded.from_orm(user)
			user_expanded.services = await UserServiceActions.get_all_services(user_uuid)
			response_model = UserExpanded
			return response_model.from_orm(user_expanded)
		return user

	@staticmethod
	async def get_service_id(new_user_obj):
		"""
		Get the service ID from the specified user object
		:param new_user_obj: The user object to get the service ID from
		:return: A namedtuple containing the service type and service ID, or None if it couldn't be found
		"""
		if (service_id := await HelperActions.get_email_from_header(new_user_obj)):
			return service_id
		elif (service_id := await HelperActions.get_cell_from_header(new_user_obj)):
			return service_id
		else:
			return None

	@classmethod
	async def create_user(cls, user):
		if isinstance(user, list):
			for user_obj in user:
				user_obj = await cls.create_user_and_service(user_obj)
		else:
			user = await cls.create_user_and_service(user)
		return user

	@classmethod
	async def create_user_and_service(cls, new_user):
		service_id = await cls.get_service_id(new_user)
		if not service_id:
			raise Exception
		user = await cls.get_user_by_service_id(service_id.value)
		if user:
			# TODO: change to "status = exists" class format
			return user
		new_user = UserModel(
			first_name = await HelperActions.get_fname_from_header(new_user),
			last_name= await HelperActions.get_lname_from_header(new_user),
			latitude = 407127281,
			longitude = -740060152,
			time_ping = int(time()),
			admin = await HelperActions.get_admin(new_user)
			time_ping = int(time())
			#time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
		)
		new_user = await cls.create(new_user)
		new_service = await UserServiceActions.create_service_for_new_user(new_user, service_id)
		if not new_service:
			raise Exception
		return new_user

	@classmethod
	async def update_user(cls, user_uuid, updates):
		return await cls.update(UserModel, [UserModel.uuid == user_uuid], updates)

	@classmethod
	async def delete_user(cls, user_uuid):
		return await cls.delete_one(UserModel, [UserModel.uuid == user_uuid])

	@classmethod
	async def delete_test_user(cls, user_uuid):
		services = await UserServiceActions.get_all_services(user_uuid)
		for key, value in services.items():
			for item in value:
				await cls.delete_one(UserServiceModelDB, [UserServiceModelDB.uuid == item.uuid])
