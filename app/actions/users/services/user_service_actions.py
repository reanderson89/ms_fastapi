from time import time
from sqlalchemy import select
from app.database.config import engine
from app.utilities import SHA224Hash
from app.routers.v1.v1CommonRouting import ExceptionHandling, CommonRoutes
from app.models.users import UserModel, UserServiceModel, UserServiceUpdate, UserServiceCreate, ServiceStatus, ServiceBase
from app.actions.helper_actions import HelperActions
from sqlalchemy.orm import Session

class UserServiceActions():

	@staticmethod
	async def check_existing(item:UserServiceCreate):
		id = item.service_user_id
		with Session(engine) as session:
			service =  session.scalars(
				select(UserServiceModel)
				.where(UserServiceModel.service_user_id == id)
				.where(UserServiceModel.user_uuid == UserModel.uuid)
			).one_or_none()
		if service:
			return ServiceStatus.from_orm(service, {"status":"exists"})
		return item

	@staticmethod
	async def check_for_existing_service_user(service_id):
		with Session(engine) as session:
			return session.scalars(
				select(UserModel)
				.where(UserServiceModel.service_user_id == service_id)
				.where(UserServiceModel.user_uuid == UserModel.uuid)
			).one_or_none()

	@classmethod
	async def create_service_user(cls, employee_data):
		employee_email = await HelperActions.get_email_from_header(employee_data)
		user = await cls.check_for_existing_service_user(employee_email)
		if user:
			return user
		#get_coordinates(employee_data["location"]) # ask Jason, is this a call to Nominatim???
		new_user = UserModel(
			first_name = await HelperActions.get_fname_from_header(employee_data),
			last_name= await HelperActions.get_lname_from_header(employee_data),
			latitude = 407127281,
			longitude = -740060152,
			time_ping= int(time()),
			#time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
		)
		new_user = await CommonRoutes.create_one_or_many(new_user)

		new_user_service = UserServiceModel(
			user_uuid = new_user.uuid,
			service_uuid = "email",
			service_user_id = employee_email,
			service_user_screenname = f"{new_user.first_name} {new_user.last_name}",
			service_user_name = await HelperActions.make_username(new_user.first_name, new_user.last_name),
			service_access_token = "access token",
			service_access_secret = "secret token",
			service_refresh_token = "refresh token",
			login_token = "place_holder",
			login_secret = "place_holder"
		)
		await CommonRoutes.create_one_or_many(new_user_service)
		return new_user

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
		await CommonRoutes.create_one_or_many(new_user_service)
		return new_user_service

	@classmethod
	async def get_service(cls, user_uuid: str, service_uuid: str):
		with Session(engine) as session:
			service = session.scalars(
				select(UserServiceModel)
				.where(
				UserServiceModel.user_uuid == user_uuid,
				UserServiceModel.uuid == service_uuid
				)
			).one_or_none()
			await ExceptionHandling.check404(service)
			return service

	@classmethod
	async def get_all_services(cls, user_uuid: str):
		with Session(engine) as session:
			services = session.scalars(
				select(UserServiceModel)
				.where(UserServiceModel.user_uuid == user_uuid)
			).all()
			await ExceptionHandling.check404(services)

		result = {}
		for service in services:
			key = service.service_uuid
			if key not in result:
				result[key] = []
			result[key].append(service)
		return result

	@classmethod
	async def create_user_service(cls, user_uuid: str, user_service):
		current_time = int(time())


		new_service = UserServiceModel(
			service_uuid = user_service.service_uuid,
			service_user_id = user_service.service_user_id
		)
		new_service.user_uuid = user_uuid
		new_service.uuid = SHA224Hash()
		new_service.time_created = current_time
		new_service.time_updated = current_time

		with Session(engine) as session:
			session.add(new_service)
			session.commit()
			session.refresh(new_service)

		service = ServiceStatus(status= "service created")
		return service.from_orm(new_service)

	@classmethod
	async def update_service(cls, user_uuid: str, service_uuid: str, updates: UserServiceUpdate):
		db_service = select(UserServiceModel).where(
			UserServiceModel.user_uuid == user_uuid,
			UserServiceModel.uuid == service_uuid
		)
		response = await HelperActions.update(db_service, updates)
		return response
