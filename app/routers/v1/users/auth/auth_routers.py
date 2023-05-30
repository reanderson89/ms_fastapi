from fastapi import APIRouter
from app.models.users import UserModel
from app.models.users.auth.auth_models import CreateAuthModel, RedeemAuthModel, AuthResponseModel
from app.actions.users.auth.auth_actions import AuthActions


router = APIRouter(tags=["Users"], prefix="/users/{user_uuid}")


@router.post("/auth", response_model=AuthResponseModel)
async def post_auth(create_auth_model: CreateAuthModel):
    return await AuthActions.post_auth_handler(create_auth_model)


@router.put("/auth/{auth}", response_model=UserModel)
async def put_auth(redeem_auth_model: RedeemAuthModel):
    return await AuthActions.redeem_auth_handler(redeem_auth_model)
