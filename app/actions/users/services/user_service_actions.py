from app.models.users import UserModel, UserServiceModel, UserServiceUpdate, UserServiceCreate, ServiceStatus
from app.actions.helper_actions import HelperActions
from app.actions.base_actions import BaseActions

class UserServiceActions(BaseActions):

	@classmethod
	async def check_existing(cls, item:UserServiceCreate):
		id = item.service_user_id

		service = await cls.check_if_exists(
			UserServiceModel,
			(
			UserServiceModel.service_user_id == id,
			UserServiceModel.user_uuid == UserModel.uuid
			)
		)

		if service:
			existing_service = ServiceStatus.from_orm(service)
			existing_service.status = "exists"
			return existing_service
		return item

	@classmethod
	async def create_service_for_new_user(cls, user, email):

		new_user_service = UserServiceModel(
			user_uuid = user.uuid,
			service_uuid = "email",
			service_user_id = email,
			service_user_screenname = f"{user.first_name} {user.last_name}",
			service_user_name = await HelperActions.make_username(user.first_name, user.last_name),
			service_access_token = "access token",
			service_access_secret = "secret token",
			service_refresh_token = "refresh token",
			login_token="place_holder",
			login_secret="place_holder"
		)
		return await cls.create(new_user_service)

	@classmethod
	async def get_service(cls, user_uuid: str, service_uuid: str):
		return await cls.get_one_where(
			UserServiceModel,
			(
			UserServiceModel.user_uuid == user_uuid,
			UserServiceModel.uuid == service_uuid
			)
		)

	@classmethod
	async def get_all_services(cls, user_uuid: str):
		services = await cls.get_all_where(
			UserServiceModel,
			(UserServiceModel.user_uuid == user_uuid,)
		)

		result = {}
		for service in services:
			key = service.service_uuid
			if key not in result:
				result[key] = []
			result[key].append(service)
		return result

	@classmethod
	async def create_user_service(cls, user_uuid: str, user_service):
		if isinstance(user_service, ServiceStatus):
			return user_service

		service_obj = UserServiceModel(
			user_uuid = user_uuid,
			service_uuid = user_service.service_uuid,
			service_user_id = user_service.service_user_id
		)
		service = await cls.create(service_obj)
		new_service = ServiceStatus.from_orm(service)
		new_service.status = "service created"
		return new_service

	@classmethod
	async def update_service(
		cls,
		user_uuid: str,
		service_uuid: str,
		updates: UserServiceUpdate
	):
		return await cls.update(
			UserServiceModel,
			(
			UserServiceModel.user_uuid == user_uuid,
			UserServiceModel.uuid == service_uuid
			),
			updates
		)

	@classmethod
	async def bulk_update_services(cls, user_uuid: str, updates: list):
		update_list = []
		for update in updates:
			db_update = UserServiceUpdate.from_orm(update)
			update_list.append(
				await cls.update_service(user_uuid, update.uuid, db_update)
			)
		return update_list

	@classmethod
	async def delete_service(cls, service_uuid: str):
		return await cls.delete(
			UserServiceModel,
			(UserServiceModel.uuid == service_uuid,)
		)

	@classmethod
	async def bulk_delete_services(cls, service_delete: list):
		deleted_services = []
		for service in service_delete:
			deleted_services.append(
				await cls.delete(
					UserServiceModel,
					(UserServiceModel.uuid == service.service_uuid,)
				)
			)
		return deleted_services
