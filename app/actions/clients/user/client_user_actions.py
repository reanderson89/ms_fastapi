from app.actions.users.services import UserServiceActions
from app.models.clients import ClientUserModel
from app.models.users import UserModel, UserServiceModel
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.utilities import SHA224Hash
from time import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine

class ClientUserActions():

	@staticmethod
	async def get_client_user_by_user_uuid(uuid: str, session: Session):
		return session.scalars(
			select(ClientUserModel)
			.where(ClientUserModel.user_uuid == uuid)
		).one_or_none()

	@classmethod
	async def createClientUser(cls, data, client_uuid, session: Session):
		user = None
		if 'email_address' not in data.keys() and 'user_uuid' not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User. Please inclue either email address or the user_uuid.")

		if 'email_address' in data.keys():
			user = session.scalars(
				select(UserModel)
				.where(UserServiceModel.service_user_id == data['email_address'])
			).one_or_none()

		if 'user_uuid' in data.keys() or user is not None:
			uuid = user.uuid if user is not None else data['user_uuid']
			client_user = await cls.get_client_user_by_user_uuid(uuid, session)
			if client_user:
				return client_user

		if not user and 'email_address' in data.keys():
			user = await UserServiceActions.create_service_user(data)

		if not user and 'email_address' not in data.keys() and 'user_uuid' not in data.keys():
			return await ExceptionHandling.custom500("Not enough information to create a new Client User, User, and Service User. Please include an email address.")

		newClientUser = ClientUserModel(
			uuid=SHA224Hash(),
			user_uuid= user.uuid,
			client_uuid= client_uuid,
			manager_uuid= data['Manager ID'] if 'Manager ID' in data else None,
			employee_id= data['Employee ID'] if 'Employee ID' in data else None,
			title= data['Business Title'] if 'Business Title' in data else None,
			department= data['Department'] if 'Department' in data else None,
			active=data['Active'] if 'Active' in data else True,
			time_hire=int(time()),
			time_start=int(time()),
			admin= data['Admin'] if 'Admin' in data else 0,
		)
		newClientUser = await CommonRoutes.create_one_or_many(newClientUser)
		return newClientUser

	@classmethod
	async def getExpandedClientUsers(cls, data, client_uuid, expansion):
		pass

	@staticmethod
	async def getAllUsers(client_uuid, session: Session):
		users = session.scalars(
			select(ClientUserModel)
			.where(ClientUserModel.client_uuid == client_uuid)
		).all()
		await ExceptionHandling.check404(users)
		return users

	@staticmethod
	async def getUser(client_uuid, user_uuid, session: Session):
		if not session:
			session = Session(engine)
		user = session.scalars(
			select(ClientUserModel)
			.where(ClientUserModel.client_uuid == client_uuid,
					UserModel.uuid == user_uuid)
		).one_or_none()
		await ExceptionHandling.check404(user)
		return user

	@staticmethod
	async def updateUser(client_uuid, user_uuid, user_updates, session: Session):
		user = session.scalars(
			select(ClientUserModel)
			.where(ClientUserModel.client_uuid == client_uuid,
					ClientUserModel.uuid == user_uuid)
			).one_or_none()
		await ExceptionHandling.check404(user)
		update_user = user_updates.dict(exclude_unset=True)
		for key, value in update_user.items():
			setattr(user, key, value)
		user.time_updated = int(time())
		session.add(user)
		session.commit()
		session.refresh(user)
		return user

	@staticmethod
	async def deleteUser(client_uuid, user_uuid, session: Session):
		user = session.scalars(
			select(ClientUserModel)
			.where(ClientUserModel.client_uuid == client_uuid,
					ClientUserModel.uuid == user_uuid)
		).one_or_none()
		await ExceptionHandling.check404(user)
		session.delete(user)
		session.commit()
		return {"ok": True, "Deleted": user}
