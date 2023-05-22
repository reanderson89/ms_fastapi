from datetime import datetime
from sqlmodel import Session, select
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.models.users import UsersModel, UserService

class UsersActions():

	@staticmethod
	def getTimeFromBday(bday):
		date_obj = datetime.strptime(bday, '%m/%d/%Y')
		epoch_time = int(date_obj.timestamp())
		return epoch_time

	@classmethod
	async def get_user_by_uuid(cls, uuid):
		with Session(engine) as session:
			return session.exec(select(UsersModel)
								.where(UsersModel.uuid == uuid)).one_or_none()

	@classmethod
	async def get_user_by_service_user_id(cls, user_id):
		with Session(engine) as session:
			return session.exec(select(UsersModel)
								.where(UserService.service_user_id == user_id)
								.where(UserService.user_uuid == UsersModel.uuid)
								).one_or_none()
