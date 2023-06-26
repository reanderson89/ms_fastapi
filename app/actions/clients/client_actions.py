from app.actions.base_actions import BaseActions
from app.models.clients import ClientModelDB, ClientUpdate

class ClientActions():

	@staticmethod
	async def get_all_clients(query_params: dict):
		return await BaseActions.get_all(ClientModelDB, query_params)

	@staticmethod
	async def get_client(client_uuid: str):
		return await BaseActions.get_one_where(
			ClientModelDB,
			[ClientModelDB.uuid == client_uuid]
		)

	@staticmethod
	async def get_client_name(client_uuid: str):
		return await BaseActions.get_one_where(
			ClientModelDB.name,
			[ClientModelDB.uuid == client_uuid]
		)

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

	@staticmethod
	async def create_client(client_data):
		client = await BaseActions.check_if_exists(
			ClientModelDB,
			[ClientModelDB.name == client_data.name]
		)
		if client:
			return client

		new_client = ClientModelDB(
			name=client_data.name,
			description=client_data.description,
			status=client_data.status,
			url=client_data.url
		)
		return await BaseActions.create(new_client)

	@staticmethod
	def update_client(client_uuid: str, update_obj: ClientUpdate):
		return BaseActions.update(
			ClientModelDB,
			[ClientModelDB.uuid ==client_uuid],
			update_obj
		)

	@staticmethod
	async def delete_client(client_uuid: str):
		return await BaseActions.delete_one(
			ClientModelDB,
			[ClientModelDB.uuid == client_uuid]
		)
