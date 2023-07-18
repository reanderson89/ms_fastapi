from app.libraries.sparkpost import send_message_email
from app.libraries.sms import send_message_text
from app.models.messages import MessageModel
from app.models.users import UserExpanded
from pybars import Compiler

compiler = Compiler()

class MessageSendingHandler():

	@classmethod
	async def send_message(cls, message: MessageModel, recipients: list) -> list:
		response = []
		for recipient in recipients:
			response.append(
					await {
					1: send_message_email,
					2: send_message_text,
					#4: await send_slack_message(message, recipients),
					#8: await send_ms_teams_message(message, recipients),
					#16: await send_web_message(message, recipients)
				}[message.channel](
					await cls.format_message_text(message.body, recipient), 
					await cls.get_service_user_id(message.channel, recipient)
				)
			)
		return response

	@staticmethod
	async def format_message_text(message: str, recipient: str) -> str:
		template = compiler.compile(message)
		message = template({
			'first_name': recipient.first_name,
			'last_name': recipient.last_name,
		})
		return message

	@staticmethod
	async def get_service_user_id(message_channel: int, recipient: UserExpanded):
		return recipient.services[
			{
				1: "email",
				2: "cell",
				# 4: "slack",
				# 8: "msteams",
				# 16: "web"
			}[message_channel]
		][0].service_user_id