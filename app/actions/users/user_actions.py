from time import time
from datetime import datetime
from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.actions.users.services import UserServiceActions
from app.models.users import UserModel, UserServiceModel, UserExpanded
from app.models.users import UserModel, UserServiceModel

class UserActions(BaseActions):

	@staticmethod
	def getTimeFromBday(bday):
		date_obj = datetime.strptime(bday, '%m/%d/%Y')
		epoch_time = int(date_obj.timestamp())
		return epoch_time

	@classmethod
	async def get_user_by_uuid(cls, uuid):
		return await cls.get_one_where(UserModel, (UserModel.uuid == uuid,))

	@classmethod
	async def get_user_by_service_id(cls, service_id):
		return await cls.check_if_exists(
			UserModel,
			(
			UserServiceModel.service_user_id == service_id,
			UserServiceModel.user_uuid == UserModel.uuid
			)
		)

	@classmethod
	async def get_all_users(cls):
		return await cls.get_all(UserModel)

	@classmethod
	async def get_user(cls, user_uuid, expand_services=False):
		user = await cls.get_user_by_uuid(user_uuid)
		if expand_services:
			user_expanded = UserExpanded.from_orm(user)
			user_expanded.services = await UserServiceActions.get_all_services(user_uuid)
			response_model = UserExpanded
			return response_model.from_orm(user_expanded)
		return user

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
		user_email = await HelperActions.get_email_from_header(new_user)
		user = await cls.get_user_by_service_id(user_email)
		if user:
			# TODO: change to status = exists class format
			return user
		new_user = UserModel(
			first_name = await HelperActions.get_fname_from_header(new_user),
			last_name= await HelperActions.get_lname_from_header(new_user),
			latitude = 407127281,
			longitude = -740060152,
			time_ping = int(time())
			#time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
		)
		new_user = await cls.create(new_user)
		new_service = await UserServiceActions.create_service_for_new_user(new_user, user_email)
		if not new_service:
			raise Exception
		return new_user


	@classmethod
	async def update_user(cls, user_uuid, updates):
		return await cls.update(UserModel, (UserModel.uuid == user_uuid,), updates)

	@classmethod
	async def delete_user(cls, user_uuid):
		return await cls.delete(UserModel, (UserModel.uuid == user_uuid,))

	@classmethod
	async def delete_test_user(cls, user_uuid):
		user = cls.delete_user(user_uuid)
		services = await UserServiceActions.get_all_services(user_uuid)
		for key, value in services.items():
			for item in value:
				await cls.delete(UserServiceModel, (UserServiceModel.uuid == item.uuid,))
