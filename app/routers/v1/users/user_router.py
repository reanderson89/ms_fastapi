import os
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Response
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.actions.users.services import UserServiceActions
from app.models.users import UsersModel, UsersUpdate, UserExpanded, UserService

test_mode = os.getenv("TEST_MODE", False)

router = APIRouter(tags=["Users"])

@router.get("/users", response_model=List[UsersModel])
async def get_users():
	return await CommonRoutes.get_all(UsersModel)

@router.get("/users/{user_uuid}", response_model_by_alias=True)
async def get_user(user_uuid: str, expand_services: bool = False):
	user = await CommonRoutes.get_one(UsersModel, user_uuid)
	if expand_services:
		user_expanded = UserExpanded.from_orm(user)
		user_expanded.services = await UserServiceActions.get_all_services(user_uuid)
		response_model = UserExpanded
		return response_model.from_orm(user_expanded)
	response_model = UsersModel
	return response_model.from_orm(user)

@router.post("/users", response_model=UsersModel)
async def create_user(users: dict):#(List[UserService] | UserService)):
	if users is List:
		for user in users:
			user = await UserServiceActions.create_service_user(user)
	else:
		users = await UserServiceActions.create_service_user(users)
	return users

@router.put("/users/{user_uuid}", response_model=UsersModel)
async def update_user(user_uuid: str, users_update: UsersUpdate):
	return await CommonRoutes.update_one(user_uuid, UsersModel, users_update)

@router.delete("/users/{user_uuid}/")
async def delete_user(user_uuid: str):
	return await CommonRoutes.delete_one(user_uuid, UsersModel)

def test_mode():
	if not test_mode:
		raise HTTPException(status_code=404, detail="Not Found")

@router.delete("/delete_test_user/{user_uuid}")
async def delete_test_user(user_uuid: str, test_mode: None = Depends(test_mode)):
	user = await CommonRoutes.delete_one(user_uuid, UsersModel)
	services = await UserServiceActions.get_all_services(user_uuid)
	for key, value in services.items():
		for item in value:
			await CommonRoutes.delete_one(item.uuid, UserService)
	return Response(status_code=200, content="Test User Deleted")
