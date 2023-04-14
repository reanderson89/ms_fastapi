from typing import List
from fastapi import APIRouter
from .users_models import UsersModel, UsersUpdate
from api import CommonRoutes

router = APIRouter()

@router.get("/users", response_model=List[UsersModel])
async def get_users():
	return CommonRoutes.get_all(UsersModel)

@router.get("/users/{user_uuid}", response_model=UsersModel)
async def get_user(user_uuid: str):
	return CommonRoutes.get_one(UsersModel, user_uuid)

@router.post("/users", response_model=UsersModel)
async def create_users(users: (UsersModel|List[UsersModel])):
	return CommonRoutes.create_one_or_many(users)

@router.put("/users/{user_uuid}")#, response_class=UsersModel)
#TODO: unable to return as the model
async def update_user(user_uuid: str, users_update: UsersUpdate):
	return CommonRoutes.update_one(user_uuid, UsersModel, users_update)
	
@router.delete("/users/{user_uuid}")
async def delete_user(user_uuid: str):
	return CommonRoutes.delete_one(user_uuid, UsersModel)
