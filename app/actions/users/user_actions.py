from time import time
from datetime import datetime
from app.actions.utils import get_location_data, convert_coordinates
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users.services import UserServiceActions
from app.models.users import UserModel, UserServiceModelDB, UserExpanded

class UserActions():

	@staticmethod
	def getTimeFromBday(bday):
		date_obj = datetime.strptime(bday, "%m/%d/%Y")
		epoch_time = int(date_obj.timestamp())
		return epoch_time

	@classmethod
	async def get_user_by_uuid(cls, uuid):
		return await BaseActions.get_one_where(UserModel, [UserModel.uuid == uuid])

	@classmethod
	async def get_user_by_service_id(cls, user_data, service_id):
		return await BaseActions.check_if_exists(
			UserModel,
			[
			UserServiceModelDB.service_user_id == service_id,
			UserServiceModelDB.user_uuid == UserModel.uuid,
			UserModel.first_name == user_data["first_name"],
			UserModel.last_name == user_data["last_name"],
			]
		)

	@classmethod
	async def get_user_by_name_and_service_id(cls, first_name, last_name, service_id):
		return await BaseActions.check_if_exists(
			UserModel,
			[
				UserModel.first_name == first_name,
				UserModel.last_name == last_name,
				UserServiceModelDB.service_user_id == service_id,
			]
		)

	@classmethod
	async def get_all_users(cls, query_params: dict):
		return await BaseActions.get_all(UserModel, query_params)

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
	async def get_service_id(new_user_obj, service_id=None):
		"""
		Get the service ID from the specified user object
		:param new_user_obj: The user object to get the service ID from
		:return: A namedtuple containing the service type and service ID, or None if it couldn't be found
		"""
		if (service_id := await HelperActions.get_email_from_header(new_user_obj, service_id)):
			return service_id
		elif (service_id := await HelperActions.get_cell_from_header(new_user_obj, service_id)):
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
	async def create_user_and_service(cls, new_user_data, service=None):
		service_id = await cls.get_service_id(new_user_data, service)

		if not service_id:
			raise Exception

		user = await cls.get_user_by_name_and_service_id(new_user_data["first_name"], new_user_data["last_name"], service_id.value)

		if user:
			# TODO: change to "status = exists" class format
			service_user = await cls.get_user_by_service_id(new_user_data, service_id.value)
			if service_user:
				return service_user
			else:
				new_service = await UserServiceActions.create_service_for_new_user(user, service_id)
				if not new_service:
					raise Exception
				return user

		# Implemented but not in use due to slow response times
		# location = get_location_data(new_user_data.get("location"))

		new_user_obj = UserModel(
			first_name = await HelperActions.get_fname_from_header(new_user_data),
			last_name= await HelperActions.get_lname_from_header(new_user_data),
			latitude = 407127281, # convert_coordinates(location.latitude),
			longitude = -740060152, # convert_coordinates(location.longitude),
			time_ping = int(time()),
			admin = await HelperActions.get_admin(new_user_data)
			#time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
		)
		user_db = await BaseActions.create(new_user_obj)
		new_service = await UserServiceActions.create_service_for_new_user(user_db, service_id)
		if not new_service:
			raise Exception
		return user_db

	@classmethod
	async def update_user(cls, user_uuid, updates):
		return await BaseActions.update(UserModel, [UserModel.uuid == user_uuid], updates)

	@classmethod
	async def delete_user(cls, user_uuid):
		return await BaseActions.delete_one(UserModel, [UserModel.uuid == user_uuid])

	@classmethod
	async def delete_test_user(cls, user_uuid):
		services = await UserServiceActions.get_all_services(user_uuid)
		for key, value in services.items():
			for item in value:
				await BaseActions.delete_one(UserServiceModelDB, [UserServiceModelDB.uuid == item.uuid])
