from sqlalchemy import select
from app.database.config import engine
from app.models.clients import ClientModel
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from sqlalchemy.orm import Session
from app.models.clients.client_budget_models import ClientBudgetModel

class ClientActions():

	@classmethod
	async def create_client_handler(cls, clients):
		to_return = []
		if isinstance(clients, list):
			for i in clients:
				client = await cls.create_client(i)
				to_return.append(client)
		else:
			client = await cls.create_client(clients)
			to_return.append(client)
		return to_return

	@classmethod
	async def create_client(cls, client_data):
		check = await cls.check_for_existing(client_data.name)
		if check:
			return check
		else:
			new_client = ClientModel(
				name=client_data.name,
				description=client_data.description,
				status=client_data.status
			)
			return await CommonRoutes.create_one_or_many(new_client)

	@classmethod
	async def check_for_existing(cls, name):
		client = await cls.get_client_by_name(name)
		if not client:
			return None
		else:
			return client

	@classmethod
	async def get_client_by_name(cls, search_by):
		with Session(engine) as session:
			return session.scalars(select(ClientModel)
								.where(ClientModel.name == search_by)).one_or_none()

	@staticmethod
	async def get_name_by_uuid(search_by):
		with Session(engine) as session:
			return session.scalars(select(ClientModel.name)
								.where(ClientModel.uuid == search_by)).one_or_none()
