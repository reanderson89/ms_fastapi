from typing import List
from fastapi import APIRouter
from app.routers.v1.v1CommonRouting import CommonRoutes
# from app.models.clients.user import ClientUserModel, ClientUserUpdate
from app.models.clients.user.client_user_models import ClientUserModel, ClientUserUpdate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Users"])

@router.post("/users", response_model=ClientUserModel)
async def create_user(users: (ClientUserModel | List[ClientUserModel])):
	return CommonRoutes.create_one_or_many(users)

@router.put("/users/{user_uuid}", response_model=ClientUserModel)
async def update_user(user_uuid: str, user_updates: ClientUserUpdate):
	return CommonRoutes.update_one(user_uuid, ClientUserModel, user_updates)

@router.delete("/users/{user_uuid}")
async def delete_user(user_uuid: str):
	#TODO: unclear if this is needed or wanted
	return CommonRoutes.delete_one(user_uuid, ClientUserModel)
