from typing import List, Union
from fastapi import APIRouter, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.models.users.services import UserService, UserServiceCreate, UsersServiceUpdate, ServiceDelete, Exists, ServiceBulk
from app.actions.users.services import UserServiceActions

router = APIRouter(tags=["Users Service"], prefix="/users/{user_uuid}")

@router.get("/services/", response_model=dict)
async def get_services(user_uuid: str):
    return await UserServiceActions.get_all_services(user_uuid)

@router.get("/services/{service_uuid}/", response_model=UserService)
async def get_service(user_uuid: str, service_uuid: str):
	return await UserServiceActions.get_service(user_uuid, service_uuid)

@router.post("/services/", response_model = Union[UserService, Exists])
async def create_service(
	user_uuid: str,
	user_service: UserServiceCreate = Depends(UserServiceActions.check_existing)
	):
	if isinstance(user_service, UserService):
		exists = Exists.from_orm(user_service)
		return exists
	response = await UserServiceActions.create_user_service(user_uuid, user_service)
	return response

@router.put("/services/{service_uuid}/", response_model=UserService)
async def update_service(user_uuid: str, service_uuid: str, service_updates: UsersServiceUpdate):
	return await UserServiceActions.update_service(user_uuid, service_uuid, service_updates)

@router.put("/services/", response_model=List[UserService])
async def bulk_update_services(user_uuid: str, updates: List[ServiceBulk]):
	update_list = []
	for update in updates:
		db_update = UsersServiceUpdate.from_orm(update)
		update_list.append(
			CommonRoutes.update_one(update.uuid, UserService, db_update)
		)
	return update_list

@router.delete("/services/{service_uuid}/")
async def delete_service(service_uuid: str):
	return CommonRoutes.delete_one(service_uuid, UserService)

@router.delete("/services/")
async def bulk_delete_service(service_delete: List[ServiceDelete]):
	deleted_services = []
	for service in service_delete:
		deleted_services.append(
			CommonRoutes.delete_one(service.service_uuid, UserService)
		)
	return deleted_services
