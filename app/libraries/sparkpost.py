import os

from app.models.users import UserServiceModelDB
from sparkpost import SparkPost
_scriptname = "ThirdParty.SparkPost"


SPARKPOST_KEY = os.environ["SPARKPOST_KEY"]
sp = SparkPost(SPARKPOST_KEY)



async def send_auth_email(user_service: UserServiceModelDB):

    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[user_service.service_user_id],
        html="<p>" + user_service.login_token + "</p>",
        from_email="no-reply@mail.blueboard.app",
        subject="Blueboard Login Token"
    )

    return response
