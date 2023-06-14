from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs.program_models import ProgramModel
from app.models.programs.program_event_models import ProgramEventModel

class ProgramEventActions():

	@staticmethod
	async def get_all_events(
		path_params, query_params
	):
		return await BaseActions.get_all_where(
			ProgramEventModel,
			[
				ProgramEventModel.client_uuid == path_params["client_uuid"],
				ProgramEventModel.program_9char == path_params["program_9char"]
			],
			query_params
		)

	@staticmethod
	async def get_event(path_params):
		return await BaseActions.get_one_where(
			ProgramEventModel,
			[
				ProgramEventModel.event_9char == path_params["event_9char"],
				ProgramEventModel.client_uuid == path_params["client_uuid"],
				ProgramEventModel.program_9char == path_params["program_9char"]
			]
		)

	@staticmethod
	async def get_program_uuid(program_9char: str):
		return await BaseActions.get_one_where(
			ProgramModel.uuid,
			[ProgramModel.program_9char == program_9char]
		)

	@staticmethod
	async def create_event(event_obj, path_params, program_uuid):
		if isinstance(event_obj, list):
			event_obj = [ProgramEventModel(
				**event.dict(),
				program_uuid = program_uuid,
				client_uuid = path_params["client_uuid"],
				program_9char = path_params["program_9char"],
				event_9char = await HelperActions.generate_9char()
			) for event in event_obj]
		else:
			event_obj = ProgramEventModel(
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
			ProgramEventModel,
			[
				ProgramEventModel.event_9char == path_params["event_9char"],
				ProgramEventModel.client_uuid == path_params["client_uuid"],
				ProgramEventModel.program_9char == path_params["program_9char"]
			],
			event_updates)

	@staticmethod
	async def delete_event(path_params):
		return await BaseActions.delete_one(
			ProgramEventModel,
			[
				ProgramEventModel.event_9char == path_params["event_9char"],
				ProgramEventModel.client_uuid == path_params["client_uuid"],
				ProgramEventModel.program_9char == path_params["program_9char"]
			]
		)
