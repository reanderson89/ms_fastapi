from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs import ProgramModelDB
from app.models.messages import MessageModelDB, MessageCreate, MessageUpdate
from app.exceptions import ExceptionHandling

class MessageActions():

	@staticmethod
	async def get_all(query_params: dict):
		return await BaseActions.get_all(MessageModelDB, query_params)

	@staticmethod
	async def get_one(message_9char: str):
		return await BaseActions.get_one_where(
			MessageModelDB,
			[MessageModelDB.message_9char == message_9char]
		)

	@staticmethod
	async def get_program_uuid(program_9char: str):
		return await BaseActions.get_one_where(
			ProgramModelDB.uuid,
			[ProgramModelDB.program_9char == program_9char]
		)
	
	@staticmethod
	async def check_for_existing_message_by_name(message, throw_error=True):
		existing_message = await BaseActions.check_if_exists(MessageModelDB, [MessageModelDB.name == message.name])
		if existing_message and throw_error:
			await ExceptionHandling.custom405(f"A message with name '{message.name}' already exists.")
		elif existing_message and not throw_error:
			return existing_message
		else:
			return message
	
	@classmethod
	async def create_message(cls, messages: MessageCreate):
		if isinstance(messages, list):
			to_create = []
			message_list = []
			for i in messages:
				message = await cls.to_message_model(i)
				message = await cls.check_for_existing_message_by_name(message, False)
				if message.uuid is None: #no message with same name exists
					to_create.append(message)
				else: #message with same name exists, appends message to list and skips a create
					message_list.append(message)
			if len(to_create) > 0:
				message_list.extend(await BaseActions.create(to_create))
			return message_list
		message = await cls.to_message_model(messages)
		message = await cls.check_for_existing_message_by_name(message, False)
		if message.uuid is None:
			return await BaseActions.create(message)
		return message
		
			
	@staticmethod
	async def to_message_model(message):
		return MessageModelDB(
			**message.dict(), 
			message_9char=await HelperActions.generate_9char()
			)

	@staticmethod
	async def send_test_message(message_9char: str):
		# TODO: Logic for sending test message
		return {"message": f"Created test message for {message_9char}"}

	@staticmethod
	async def send_message(message_9char: str):
		# TODO: Logic for sending message to program audience
		return {"message": f"Sent message for {message_9char}"}

	@classmethod
	async def update_message(cls, message_9char: str, message_updates: MessageUpdate):
		if message_updates.name:
			await cls.check_for_existing_message_by_name(message_updates, True)
		return await BaseActions.update(
			MessageModelDB, 
			[MessageModelDB.message_9char == message_9char],
			message_updates
		)

	@staticmethod
	async def delete_message(message_9char: str):
		message = await BaseActions.get_one_where(MessageModelDB, [MessageModelDB.message_9char == message_9char])
		if message.client_uuid and message.status == 2: #status of 2 indicates "published"
			return await ExceptionHandling.custom405(f"Cannot delete client message {message.name}, status code is published.")
		return await BaseActions.delete_one(
			MessageModelDB, [MessageModelDB.message_9char == message_9char]
		)
