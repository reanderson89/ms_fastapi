from app.actions.base_actions import BaseActions
from app.models.programs.program_award_models import ProgramAwardModel, ProgramAwardUpdate


class ProgramAwardActions():

	@staticmethod
	async def get_program_awards(path_params: dict, query_params: dict):
		return await BaseActions.get_all_where(
			ProgramAwardModel,
			[
				ProgramAwardModel.client_uuid == path_params["client_uuid"],
				ProgramAwardModel.program_9char == path_params["program_9char"],
			],
			query_params
		)

	@staticmethod
	async def get_award(path_params: dict):
		return await BaseActions.get_one_where(
			ProgramAwardModel,
			[
				ProgramAwardModel.client_uuid == path_params["client_uuid"],
				ProgramAwardModel.program_9char == path_params["program_9char"],
				ProgramAwardModel.program_award_9char == path_params["program_award_9char"]
			],
		)

	@staticmethod
	async def create_award(path_params: dict, award_obj):
		if isinstance(award_obj, list):
			award_models = [
				ProgramAwardModel(
					**award.dict(),
					client_uuid=path_params["client_uuid"],
					program_9char=path_params["program_9char"],
					client_award_9char=path_params["client_award_9char"]
				) for award in award_obj
			]
		else:
			award_models = ProgramAwardModel(
				**award_obj.dict(),
				client_uuid=path_params["client_uuid"],
				program_9char=path_params["program_9char"],
				client_award_9char=path_params["client_award_9char"]
			)
		return await BaseActions.create(award_models)


	@staticmethod
	async def update_award(
		path_params: dict,
		award_updates: ProgramAwardUpdate
	):
		return await BaseActions.update(
			ProgramAwardModel,
			[
				ProgramAwardModel.client_uuid == path_params["client_uuid"],
				ProgramAwardModel.program_9char == path_params["program_9char"],
				ProgramAwardModel.program_award_9char == path_params["program_award_9char"]
			],
			award_updates
		)

	@staticmethod
	async def delete_award(path_params: dict):
		return await BaseActions.delete_one(
			ProgramAwardModel,
			[
				ProgramAwardModel.client_uuid == path_params["client_uuid"],
				ProgramAwardModel.program_9char == path_params["program_9char"],
				ProgramAwardModel.program_award_9char == path_params["program_award_9char"]
			],
		)
