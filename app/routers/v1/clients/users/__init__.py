from app.models.clients.user import ClientUserModel, ClientUserUpdate
from app.routers.v1.v1CommonRouting import CommonRoutes
from typing import List
from fastapi import APIRouter

router = APIRouter()

@router.post("/clients/{client_uuid}/users", response_model=ClientUserModel)
async def create_user(users: (ClientUserModel | List[ClientUserModel])):
	return CommonRoutes.create_one_or_many(users)

@router.put("/clients/{client_uuid}/users/{user_uuid}", response_model=ClientUserModel)
async def update_user(user_uuid: str, user_updates: ClientUserUpdate):
	return CommonRoutes.update_one(user_uuid, ClientUserModel, user_updates)

@router.delete("/clients/{client_uuid}/users/{user_uuid}")
async def delete_user(user_uuid: str):
	#TODO: unclear if this is needed or wanted
	return CommonRoutes.delete_one(user_uuid, ClientUserModel)
