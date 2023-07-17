from fastapi import APIRouter, Response
from app.models.users import UserModel, UserBase
from app.models.users.auth.auth_models import CreateAuthModel, RedeemAuthModel, AuthResponseModel
from app.actions.users.auth.auth_actions import AuthActions
from app.utilities.auth.auth_handler import access_token_creation

router = APIRouter()


@router.post("/auth", response_model=AuthResponseModel)
async def post_auth(create_auth_model: CreateAuthModel):
    return await AuthActions.post_auth_handler(create_auth_model)


@router.put("/auth/{auth}", response_model=UserModel)
async def put_auth(redeem_auth_model: RedeemAuthModel, response: Response):
    redeem_return = await AuthActions.redeem_auth_handler(redeem_auth_model)
    user_model = dict(UserBase.from_orm(redeem_return))
    client_uuid = await AuthActions.grab_admin_level(user_model)
    user_model['client_uuid'] = client_uuid
    bearer_token = await access_token_creation(user_model)
    response.headers["Bearer"] = bearer_token["access_token"]

    return redeem_return
