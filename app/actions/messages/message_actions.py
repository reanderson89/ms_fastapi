from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.clients.client_user_models import ClientUserModelDB
from app.models.programs import ProgramModelDB
from app.models.messages import MessageModelDB, MessageCreate, MessageUpdate, MessageSend
from app.exceptions import ExceptionHandling
from app.actions.messages.send_message import MessageSendingHandler
from app.actions.users.user_actions import UserActions


class MessageActions():

	@staticmethod
	async def get_all(query_params: dict):
		return await BaseActions.get_all(MessageModelDB, query_params)
	
	@staticmethod
	async def get_all_client_messages(client_uuid: str, query_params: dict):
		return await BaseActions.get_all_where(
			MessageModelDB,
			[
				MessageModelDB.client_uuid == client_uuid
			],
			query_params
		)

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
	

	@classmethod
	async def send_message(cls, message_9char: str, send_model: MessageSend):
		message = await cls.get_one(message_9char)
		recipients_models = await BaseActions.get_all_where(
			ClientUserModelDB,
			[ClientUserModelDB.uuid.in_(send_model.recipients)],
			None,
			False,
			False
		)
		user_uuids = [i.user_uuid for i in recipients_models]
		service_id_type = {
			1: "email", #email
			2: "cell", #sms - text
			4: "slack", #p2p - slack
			8: "msteams", #p2p - ms teams
			16: "web" #web
		}[message.channel]
		recipients = await cls.get_user_and_service(user_uuids, service_id_type)
		return await MessageSendingHandler.send_message(message, recipients)
	
	
	@classmethod
	async def get_user_and_service(cls, user_uuids: list, service_id_type: str):
		users = []
		for uuid in user_uuids:
			users.append(await UserActions.get_user(uuid, True))
		return users
