from fastapi import APIRouter, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.models.users import UserServiceUpdate, UserServiceModel, UserServiceCreate, ServiceDelete, ServiceStatus, ServiceBulk
from app.actions.users.services import UserServiceActions
from app.actions.helper_actions import HelperActions

router = APIRouter(tags=["Users Service"], prefix="/users/{user_uuid}")

@router.get("/services", response_model=dict)
async def get_services(user_uuid: str):
    return await UserServiceActions.get_all_services(user_uuid)

@router.get("/services/{service_uuid}", response_model=UserServiceModel)
async def get_service(user_uuid: str, service_uuid: str):
	return await UserServiceActions.get_service(user_uuid, service_uuid)

@router.post("/services", response_model=ServiceStatus)
async def create_service(
	user_uuid: str,
	user_service: UserServiceCreate = Depends(UserServiceActions.check_existing)
):
	if isinstance(user_service, ServiceStatus):
		return user_service
	return await UserServiceActions.create_user_service(user_uuid, user_service)

@router.put("/services/{service_uuid}", response_model=UserServiceModel)
async def update_service(
	user_uuid: str,
	service_uuid: str,
	service_updates: UserServiceUpdate
):
	return await UserServiceActions.update_service(user_uuid, service_uuid, service_updates)

@router.put("/services/", response_model=list[UserServiceModel])
async def bulk_update_services(user_uuid: str, updates: list[ServiceBulk]):
	update_list = []
	for update in updates:
		db_update = UserServiceUpdate.from_orm(update)
		update_list.append(
			await CommonRoutes.update_one(update.uuid, UserServiceModel, db_update)
		)
	return update_list

@router.delete("/services/{service_uuid}")
async def delete_service(service_uuid: str):
	return await CommonRoutes.delete_one(service_uuid, UserServiceModel)

@router.delete("/services")
async def bulk_delete_service(service_delete: list[ServiceDelete]):
	deleted_services = []
	for service in service_delete:
		deleted_services.append(
			await CommonRoutes.delete_one(service.service_uuid, UserServiceModel)
		)
	return deleted_services
