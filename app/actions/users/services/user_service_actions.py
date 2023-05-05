import codecs, csv, json
from time import time
from fastapi import UploadFile, File
from sqlmodel import Session, select
from app.database.config import engine
from app.utilities import SHA224Hash
from app.routers.v1.v1CommonRouting import ExceptionHandling, CommonRoutes
from app.models.users import UsersModel
from app.actions.users import UsersActions
from app.models.users.services import UserService, UserServiceCreate, UsersServiceUpdate

class UserServiceActions():

	@staticmethod
	async def check_existing(item:UserServiceCreate):
		id = item.service_user_id
		with Session(engine) as session:
			result =  session.exec(
				select(UserService)
				.where(UserService.service_user_id == id)
				.where(UserService.user_uuid == UsersModel.uuid)
			).one_or_none()
		if result:
			return result
		return item

	@staticmethod
	def make_username(first, last):
		first = first.lower()
		last = last.lower()
		return f"{first}{last}"

	@classmethod
	async def process_csv(cls, csv_file: UploadFile = File(...)):
			csv_reader = csv.DictReader(codecs.iterdecode(csv_file.file, 'utf-8'))
			users = []
			for row in csv_reader:
				user_data = json.loads(json.dumps(row))
				user = await cls.create_service_user(user_data)
				users.append(user)
			return users

	@classmethod
	async def create_service_user(cls, employee_data):
		if 'Primary Work Email' in employee_data or 'primary_work_email' in employee_data:
			employee_email = employee_data.get('Primary Work Email') or employee_data.get('primary_work_email')
		else:
			raise Exception
		print(employee_email)
		user = await UsersActions.check_for_existing(employee_email)
		if user:
			return user
		elif not user:
			#get_coordinates(employee_data["location"]) # ask Jason, is this a call to Nominatim???
			new_user = UsersModel(
				first_name = (employee_data['legal_first_name'] or employee_data['Legal First Name']),
				last_name= (employee_data['legal_last_name'] or employee_data['Legal Last Name']),
				latitude = 407127281,
				longitude = -740060152,
				time_ping= int(time()),
				time_birthday=  UsersActions.getTimeFromBday(employee_data['hire_date'] or employee_data['Hire Date']),
			)
			new_user = CommonRoutes.create_one_or_many(new_user)

			new_user_service = UserService(
				user_uuid = new_user.uuid,
				service_uuid = SHA224Hash(),
				service_user_id = employee_email,
				service_user_screenname = f"{new_user.first_name} {new_user.last_name}",
				service_user_name = cls.make_username(new_user.first_name, new_user.last_name),
				service_access_token = "access token",
				service_access_secret = "secret token",
				service_refresh_token = "refresh token",
			)
			CommonRoutes.create_one_or_many(new_user_service)
			return new_user # or add to list of users

	@classmethod
	async def get_service(cls, user_uuid: str, service_uuid: str):
		with Session(engine) as session:
			service = session.exec(
				select(UserService)
				.where(
				UserService.user_uuid == user_uuid,
				UserService.uuid == service_uuid
				)
			).one_or_none()
			ExceptionHandling.check404(service)
			return service

	@classmethod
	async def get_all_services(cls, user_uuid: str):
		with Session(engine) as session:
			services = session.exec(
				select(UserService)
				.where(UserService.user_uuid == user_uuid)
			).all()
			ExceptionHandling.check404(services)

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
			return new_service

	@classmethod
	async def update_service(cls, user_uuid: str, service_uuid: str, updates: UsersServiceUpdate):
		db_service = select(UserService).where(
			UserService.user_uuid == user_uuid,
			UserService.uuid == service_uuid
		)
		response = cls.update(db_service, updates)
		return response

	@staticmethod
	def update(statement, updates):
		with Session(engine) as session:
			response = session.exec(statement).one_or_none()
			ExceptionHandling.check404(response)

			updated_fields = updates.dict(exclude_unset=True)
			for key, value in updated_fields.items():
				setattr(response, key, value)
			session.add(response)
			session.commit()
			session.refresh(response)
			return response
