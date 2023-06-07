from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs import ProgramModel
from app.models.messages import MessageModel, MessageCreate, MessageUpdate


class MessageActions():

	@staticmethod
	async def get_all(path_params: dict, query_params: dict):
		return await BaseActions.get_all_where(
			MessageModel,
			[
				MessageModel.client_uuid == path_params['client_uuid'],
				MessageModel.program_9char == path_params['program_9char']
			],
			query_params
		)

	@staticmethod
	async def get_one(path_params: dict):
		return await BaseActions.get_one_where(
			MessageModel,
			[
				MessageModel.client_uuid == path_params['client_uuid'],
				MessageModel.program_9char == path_params['program_9char'],
				MessageModel.message_9char == path_params['message_9char']
			]
		)

	@staticmethod
	async def get_program_uuid(program_9char: str):
		return await BaseActions.get_one_where(
			ProgramModel.uuid,
			[ProgramModel.program_9char == program_9char]
		)

	@staticmethod
	async def create_message(message: MessageCreate, path_params: dict, program_uuid: str):
		new_message = MessageModel(
			**message.dict(),
			program_uuid=program_uuid,
			client_uuid=path_params['client_uuid'],
			program_9char=path_params['program_9char'],
			message_9char=await HelperActions.generate_9char(),
			)
		return await BaseActions.create(new_message)

	@staticmethod
	async def send_test_message(message_9char: str):
		# TODO: Logic for sending test message
		return {"message": f"Created test message for {message_9char}"}

	@staticmethod
	async def send_message(message_9char: str):
		# TODO: Logic for sending message to program audience
		return {"message": f"Sent message for {message_9char}"}

	@staticmethod
	async def update_message(path_params: dict, message_updates: MessageUpdate):
		return await BaseActions.update(
			MessageModel,
			[
				MessageModel.client_uuid == path_params['client_uuid'],
				MessageModel.program_9char == path_params['program_9char'],
				MessageModel.message_9char == path_params['message_9char']
			],
			message_updates
		)

	@staticmethod
	async def delete_message(path_params: dict):
		return await BaseActions.delete_one(
			MessageModel,
			[
				MessageModel.client_uuid == path_params['client_uuid'],
				MessageModel.program_9char == path_params['program_9char'],
				MessageModel.message_9char == path_params['message_9char']
			]
		)
