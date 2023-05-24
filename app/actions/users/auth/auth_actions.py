import random
from uuid import uuid4

from app.actions.commonActions import CommonActions
from app.actions.users.services import UserServiceActions
from app.models.users import UserService, UsersServiceUpdate
from app.models.users.auth.auth_models import CreateAuthModel, AuthResponseModel, RedeemAuthModel
from app.database.config import engine
from app.actions.users import UsersActions
from app.routers.v1.v1CommonRouting import ExceptionHandling
from sqlalchemy.orm import Session
from sqlalchemy import select


class AuthActions():

    @classmethod
    async def post_auth_handler(cls, auth_model: CreateAuthModel):
        check_user_service = await cls.post_auth_creation(auth_model)
        print('above')
        print(check_user_service)
        if check_user_service:
            new_auth_response = AuthResponseModel(
                login_secret=check_user_service.login_secret,
                login_token=check_user_service.login_token,
                service_user_id=check_user_service.service_user_id,
                service_uuid=check_user_service.service_uuid
            )
            return new_auth_response

    @classmethod
    async def post_auth_creation(cls, auth_model):
        with Session(engine) as session:
            service = session.scalars(
                select(UserService)
                .where(UserService.service_uuid == auth_model.service_uuid)
                .where(UserService.service_user_id == auth_model.service_user_id)
            ).one_or_none()
            await ExceptionHandling.check404(service)

            auth_object = await cls.generate_auth(service)

            updates = UsersServiceUpdate(
                login_token=auth_object.login_token,
                login_secret=auth_object.login_secret
            )

            response = await UserServiceActions.update_service(
                auth_object.user_uuid,
                auth_object.uuid,
                updates
            )

            return response

    @classmethod
    async def redeem_auth_handler(cls, redeem_auth_model):
        check_redeem = await cls.check_for_match_put(redeem_auth_model)
        if check_redeem:
            return await UsersActions.get_user_by_uuid(check_redeem.user_uuid)
        else:
            return check_redeem

    @classmethod
    async def check_for_match_put(cls, redeem_auth_model: RedeemAuthModel):
        with Session(engine) as session:
            service = session.scalars(
                select(UserService)
                .where(UserService.login_token == redeem_auth_model.login_token)
                .where(UserService.login_secret == redeem_auth_model.login_secret)
            ).one_or_none()
            await ExceptionHandling.check404(service)
            return service

    @classmethod
    async def generate_auth(cls, user_service_model):
        if user_service_model.service_uuid == "email":
            user_service_model.login_token = uuid4().hex
            user_service_model.login_secret = uuid4().hex

        else:
            user_service_model.login_token = str(random.randint(1000, 9999))
            user_service_model.login_secret = uuid4().hex

        return user_service_model



