from typing import List, Union
from fastapi import APIRouter, UploadFile, File
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.actions.users.services import UserServiceActions
from app.models.users import UsersModel, UsersUpdate, UserExpanded
from app.actions.commonActions import CommonActions

router = APIRouter(tags=["Users"])

@router.get("/users/", response_model=List[UsersModel])
async def get_users():
	return CommonRoutes.get_all(UsersModel)

@router.get("/users/{user_uuid}", response_model_by_alias=True)
async def get_user(user_uuid: str, expand_services: bool = False):
	user = CommonRoutes.get_one(UsersModel, user_uuid)
	if expand_services:
		user_expanded = UserExpanded.from_orm(user)
		user_expanded.services = await UserServiceActions.get_all_services(user_uuid)
		response_model = UserExpanded
		return response_model.from_orm(user_expanded)
	response_model = UsersModel
	return response_model.from_orm(user)

@router.post("/users/", response_model=UsersModel)
async def create_user(users: Union[List[UsersModel], UsersModel]):
	if isinstance(users, UsersModel):
		users = await UserServiceActions.create_service_user(users)
		return users
	else:
		created_users = []
		for user in users:
			created_users.append(await UserServiceActions.create_service_user(user))
		return created_users

@router.post("/users/upload/")
async def user_service(user_data: UploadFile = File(...)):
	return await CommonActions.process_csv(user_data)

@router.put("/users/{user_uuid}", response_model=UsersModel)
async def update_user(user_uuid: str, users_update: UsersUpdate):
	return CommonRoutes.update_one(user_uuid, UsersModel, users_update)

@router.delete("/users/{user_uuid}")
async def delete_user(user_uuid: str):
	return CommonRoutes.delete_one(user_uuid, UsersModel)
