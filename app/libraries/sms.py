import os

from app.models.users import UserServiceModelDB
from twilio.rest import Client


ACCOUNT_TOKEN = os.environ["ACCOUNT_TOKEN"]
ACCOUNT_SID = os.environ["ACCOUNT_SID"]
TWILIO_FROM = os.environ["TWILIO_FROM"]
TwilioClient = Client(ACCOUNT_SID, ACCOUNT_TOKEN)


async def send_sms_worker(user_service: UserServiceModelDB):

	message = TwilioClient.messages.create(
		to="+1" + user_service.service_user_id,
		from_=TWILIO_FROM,
		body=user_service.login_token
	)

	return message.sid


async def send_message_text(message: str, recipients: list):
	message_sid = []
	for recipient in recipients:
		message = TwilioClient.messages.create(
			to="+1" + recipient,
			from_=TWILIO_FROM,
			body=message.body
		)
		message_sid.append({recipient: message.sid})

	return message_sid
