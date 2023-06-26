from app.actions.base_actions import BaseActions
from app.models.clients.client_award_models import ClientAwardModelDB, ClientAwardUpdate


class ClientAwardActions():

	@staticmethod
	async def get_client_awards(client_uuid: str, query_params: dict):
		return await BaseActions.get_all_where(
			ClientAwardModelDB,
			[ClientAwardModelDB.client_uuid == client_uuid],
			query_params
		)

	@staticmethod
	async def get_award(client_uuid: str, client_award_9char: str):
		return await BaseActions.get_one_where(
			ClientAwardModelDB,
			[
				ClientAwardModelDB.client_award_9char == client_award_9char,
				ClientAwardModelDB.client_uuid == client_uuid
			]
		)

	@staticmethod
	async def create_award(client_uuid: str, award_obj):
		if isinstance(award_obj, list):
			award_models = [
				ClientAwardModelDB(
					**award.__dict__, client_uuid=client_uuid
				) for award in award_obj
			]
		else:
			award_models = ClientAwardModelDB(
				**award_obj.__dict__,
				client_uuid = client_uuid
			)
		return await BaseActions.create(award_models)


	@staticmethod
	async def update_award(
		client_uuid: str,
		client_award_9char: str,
		award_updates: ClientAwardUpdate
	):
		return await BaseActions.update(
			ClientAwardModelDB,
			[
				ClientAwardModelDB.client_award_9char == client_award_9char,
				ClientAwardModelDB.client_uuid == client_uuid
			],
			award_updates
		)

	@staticmethod
	async def delete_award(client_uuid: str, client_award_9char: str):
		return await BaseActions.delete_one(
			ClientAwardModelDB,
			[
				ClientAwardModelDB.client_award_9char == client_award_9char,
				ClientAwardModelDB.client_uuid == client_uuid
			]
		)
