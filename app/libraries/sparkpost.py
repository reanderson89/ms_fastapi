import os

from app.models.users import UserServiceModelDB
from app.models.messages import MessageModel
from sparkpost import SparkPost
_scriptname = "ThirdParty.SparkPost"


SPARKPOST_KEY = os.environ["SPARKPOST_KEY"]
sp = SparkPost(SPARKPOST_KEY)

BASE_URL = os.getenv("BASE_URL", "https://milestones.blueboard.app")
REDEEM_URL = f"{BASE_URL}/auth/verify-email-token?token="

async def send_auth_email(user_service: UserServiceModelDB):

    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[user_service.service_user_id],
        html="<a href=" + REDEEM_URL + user_service.login_token + ">VERIFY EMAIL</a>",
        from_email="no-reply@mail.blueboard.app",
        subject="Blueboard Login Token"
    )

    return response

async def send_message_email(message: str, recipient: str):

    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[recipient],
        html=message,
        from_email="no-reply@mail.blueboard.app",
        subject="Blueboard Message",
    )

    return response