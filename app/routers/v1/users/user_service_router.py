from fastapi import APIRouter, Depends
from app.models.users import UserServiceUpdate, UserServiceModel, UserServiceCreate, ServiceDelete, ServiceStatus, ServiceBulk
from app.actions.users.services import UserServiceActions

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
	return await UserServiceActions.create_user_service(user_uuid, user_service)


@router.put("/services/{service_uuid}", response_model=UserServiceModel)
async def update_service(
	user_uuid: str,
	service_uuid: str,
	service_updates: UserServiceUpdate
):
	return await UserServiceActions.update_service(user_uuid, service_uuid, service_updates)


@router.put("/services", response_model=list[UserServiceModel])
async def bulk_update_services(user_uuid: str, updates: list[ServiceBulk]):
	return await UserServiceActions.bulk_update_services(user_uuid, updates)


@router.delete("/services/{service_uuid}")
async def delete_service(service_uuid: str):
	return await UserServiceActions.delete_service(service_uuid)


@router.delete("/services")
async def bulk_delete_service(service_delete: list[ServiceDelete]):
	return await UserServiceActions.bulk_delete_services(service_delete)
