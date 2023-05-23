from time import time
from sqlalchemy import select
from app.database.config import engine
from app.utilities import SHA224Hash
from app.routers.v1.v1CommonRouting import ExceptionHandling, CommonRoutes
from app.models.users import UsersModel
from app.actions.users import UsersActions
from app.models.users import UserService, UsersServiceUpdate, UserServiceCreate, ServiceStatus
from app.actions.commonActions import CommonActions
from sqlalchemy.orm import Session

class UserServiceActions():

	@staticmethod
	async def check_existing(item:UserServiceCreate):
		id = item.service_user_id
		with Session(engine) as session:
			service =  session.scalars(
				select(UserService)
				.where(UserService.service_user_id == id)
				.where(UserService.user_uuid == UsersModel.uuid)
			).one_or_none()
		if service:
			return ServiceStatus.from_orm(service, {"status":"exists"})
		return item

	@staticmethod
	async def check_service_id_for_existing_service_user(service_id):
		with Session(engine) as session:
			return session.scalars(
				select(UsersModel)
				.where(UserService.service_user_id == service_id)
			).one_or_none()

	@classmethod
	async def create_service_user(cls, employee_data):
		employee_email = await CommonActions.get_email_from_header(employee_data)
		user = await cls.check_service_id_for_existing_service_user(employee_email)
		if user:
			return user
		elif not user:
			#get_coordinates(employee_data["location"]) # ask Jason, is this a call to Nominatim???
			new_user = UsersModel(
				first_name = await CommonActions.get_fname_from_header(employee_data),
				last_name= await CommonActions.get_lname_from_header(employee_data),
				latitude = 407127281,
				longitude = -740060152,
				time_ping= int(time()),
				#time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
			)
			new_user = await CommonRoutes.create_one_or_many(new_user)

			new_user_service = UserService(
				user_uuid = new_user.uuid,
				service_uuid = "email",
				service_user_id = employee_email,
				service_user_screenname = f"{new_user.first_name} {new_user.last_name}",
				service_user_name = await CommonActions.make_username(new_user.first_name, new_user.last_name),
				service_access_token = "access token",
				service_access_secret = "secret token",
				service_refresh_token = "refresh token",
			)
			await CommonRoutes.create_one_or_many(new_user_service)
			return new_user

	@classmethod
	async def get_service(cls, user_uuid: str, service_uuid: str):
		with Session(engine) as session:
			service = session.scalars(
				select(UserService)
				.where(
				UserService.user_uuid == user_uuid,
				UserService.uuid == service_uuid
				)
			).one_or_none()
			await ExceptionHandling.check404(service)
			return service

	@classmethod
	async def get_all_services(cls, user_uuid: str):
		with Session(engine) as session:
			services = session.scalars(
				select(UserService)
				.where(UserService.user_uuid == user_uuid)
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
		new_service = UserService.from_orm(user_service)
		new_service.user_uuid = user_uuid
		new_service.uuid = SHA224Hash()
		new_service.time_created = current_time
		new_service.time_updated = current_time

		with Session(engine) as session:
			session.add(new_service)
			session.commit()
			session.refresh(new_service)

		return ServiceStatus.from_orm(new_service, {"status":"service created"})

	@classmethod
	async def update_service(cls, user_uuid: str, service_uuid: str, updates: UsersServiceUpdate):
		db_service = select(UserService).where(
			UserService.user_uuid == user_uuid,
			UserService.uuid == service_uuid
		)
		response = await CommonActions.update(db_service, updates)
		return response
