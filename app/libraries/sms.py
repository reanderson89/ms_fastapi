import os

from app.models.users import UserServiceModel
from twilio.rest import Client


ACCOUNT_TOKEN = os.environ["ACCOUNT_TOKEN"]
ACCOUNT_SID = os.environ["ACCOUNT_SID"]
TWILIO_FROM = os.environ["TWILIO_FROM"]
TwilioClient = Client(ACCOUNT_SID, ACCOUNT_TOKEN)


async def send_sms_worker(user_service: UserServiceModel):

	message = TwilioClient.messages.create(
		to="+1" + user_service.service_user_id,
		from_=TWILIO_FROM,
		body=user_service.login_token
	)

	return message.sid

