import os

from fastapi import APIRouter, Path
from app.models.clients.client_user_models import ClientUserResponse
from app.actions.clients.user.client_user_actions import ClientUserActions

router = APIRouter(tags=["Auth"])

ENV: str = os.environ.get("ENV", "local")
JWT_ENFORCED: str = os.environ.get("JWT_ENFORCED", 'False').lower()


# @router.post("/auth", response_model=AuthResponseModel)
# async def post_auth(create_auth_model: CreateAuthModel):
#     return_model = await AuthActions.post_auth_handler(create_auth_model)
#     if JWT_ENFORCED == "false":
#         return return_model
#     else:
#         prod_return = AuthResponseModel(
#             login_secret=return_model.login_secret,
#             service_uuid=return_model.service_uuid,
#             service_user_id=return_model.service_user_id
#         )
#         return prod_return


# @router.put("/auth/{auth}", response_model=UserModelDB)
# async def put_auth(redeem_auth_model: RedeemAuthModel, response: Response):
#     redeem_return = await AuthActions.redeem_auth_handler(redeem_auth_model)
#     user_model = dict(UserModel.from_orm(redeem_return))
#     client_uuid = await AuthActions.grab_admin_level(user_model)
#     user_model["client_uuid"] = client_uuid
#     bearer_token = await access_token_creation(user_model)
#     response.headers["Bearer"] = bearer_token["access_token"]

#     return redeem_return

@router.get("/auth/client_user/{user_uuid}", response_model=ClientUserResponse)
async def get_client_user(
    user_uuid: str = Path(...)
):
    return await ClientUserActions.auth_get_user(user_uuid)
