from app.actions.base_actions import BaseActions
from app.models.clients import ClientModel, ClientUpdate

class ClientActions(BaseActions):

	@classmethod
	async def get_all_clients(cls, query_params: dict):
		return await cls.get_all(ClientModel, query_params)

	@classmethod
	async def get_client(cls, client_uuid: str):
		return await cls.get_one_where(
			ClientModel,
			[ClientModel.uuid == client_uuid]
		)

	@classmethod
	async def get_client_name(cls, client_uuid: str):
		return await cls.get_one_where(
			ClientModel.name,
			[ClientModel.uuid == client_uuid]
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

	@classmethod
	async def create_client(cls, client_data):
		client = await cls.check_if_exists(
			ClientModel,
			[ClientModel.name == client_data.name]
		)
		if client:
			return client

		new_client = ClientModel(
			name=client_data.name,
			description=client_data.description,
			status=client_data.status
		)
		return await cls.create(new_client)

	@classmethod
	def update_client(cls, client_uuid: str, update_obj: ClientUpdate):
		return cls.update(
			ClientModel,
			[ClientModel.uuid ==client_uuid],
			update_obj
		)

	@classmethod
	async def delete_client(cls, client_uuid: str):
		return await cls.delete_one(
			ClientModel,
			[ClientModel.uuid == client_uuid]
		)
