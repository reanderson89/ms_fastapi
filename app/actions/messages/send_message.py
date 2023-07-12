import json
from typing import Optional
from app.actions.clients.user import ClientUserActions
from app.actions.users.services.user_service_actions import UserServiceActions


from app.libraries.sparkpost import send_message_email
from app.libraries.sms import send_message_text

from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs import ProgramModelDB
from app.models.messages import MessageModel
from app.exceptions import ExceptionHandling

class MessageSendingHandler():

	@classmethod
	async def send_message(cls, message: MessageModel, recipients: list) -> list:
		return await {
			1: send_message_email,
			2: send_message_text,
			#4: await send_slack_message(message, recipients),
			#8: await send_ms_teams_message(message, recipients),
			#16: await send_web_message(message, recipients)
		}[message.channel](message, recipients)
		

	@staticmethod
	async def create_message_from_template(message_9char: str):
		pass

	#returns the message template with the handlebars not replaced with values
	@staticmethod
	async def get_message_template(message_9char: str):
		pass

	#returns the message template with the handlebars replaced with values
	@staticmethod
	async def get_message_template_with_values(message_9char: str, message_values: dict):
		pass