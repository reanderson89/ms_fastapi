from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs.program_models import ProgramModelDB
from app.models.programs.program_event_models import ProgramEventModelDB

class ProgramEventActions():

	@staticmethod
	async def get_all_events(
		path_params, query_params
	):
		return await BaseActions.get_all_where(
			ProgramEventModelDB,
			[
				ProgramEventModelDB.client_uuid == path_params["client_uuid"],
				ProgramEventModelDB.program_9char == path_params["program_9char"]
			],
			query_params
		)

	@staticmethod
	async def get_event(path_params):
		return await BaseActions.get_one_where(
			ProgramEventModelDB,
			[
				ProgramEventModelDB.event_9char == path_params["event_9char"],
				ProgramEventModelDB.client_uuid == path_params["client_uuid"],
				ProgramEventModelDB.program_9char == path_params["program_9char"]
			]
		)

	@staticmethod
	async def get_program_uuid(program_9char: str):
		return await BaseActions.get_one_where(
			ProgramModelDB.uuid,
			[ProgramModelDB.program_9char == program_9char]
		)

	@staticmethod
	async def create_event(event_obj, path_params, program_uuid):
		if isinstance(event_obj, list):
			event_objs = [ProgramEventModelDB(
				**event.dict(),
				program_uuid = program_uuid,
				client_uuid = path_params["client_uuid"],
				program_9char = path_params["program_9char"],
				event_9char = await HelperActions.generate_9char()
			) for event in event_obj]
			return await BaseActions.create(event_objs)
		event_obj = ProgramEventModelDB(
			**event_obj.dict(),
			program_uuid = program_uuid,
			client_uuid = path_params["client_uuid"],
			program_9char = path_params["program_9char"],
			event_9char = await HelperActions.generate_9char()
		)
		return await BaseActions.create(event_obj)

	@staticmethod
	async def update_event(event_updates, path_params):
		return await BaseActions.update(
			ProgramEventModelDB,
			[
				ProgramEventModelDB.event_9char == path_params["event_9char"],
				ProgramEventModelDB.client_uuid == path_params["client_uuid"],
				ProgramEventModelDB.program_9char == path_params["program_9char"]
			],
			event_updates)

	@staticmethod
	async def delete_event(path_params):
		return await BaseActions.delete_one(
			ProgramEventModelDB,
			[
				ProgramEventModelDB.event_9char == path_params["event_9char"],
				ProgramEventModelDB.client_uuid == path_params["client_uuid"],
				ProgramEventModelDB.program_9char == path_params["program_9char"]
			]
		)
