from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.models.clients import ClientUserModelDB, ClientUserUpdate, ClientUserModel
from app.actions.clients.user import ClientUserActions


router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Users"])


def path_params(client_uuid: str, user_uuid: str=None):
	return {
		"client_uuid": client_uuid,
		"user_uuid": user_uuid
	}


@router.get("/users")
async def get_users(
	client_uuid: str,
	query_params: dict = Depends(default_query_params)
) -> Page[ClientUserModel]:
	return await ClientUserActions.get_all_users(client_uuid, query_params)


@router.get("/users/{user_uuid}", response_model=ClientUserModelDB)
async def get_user(path_params: dict = Depends(path_params)):
	return await ClientUserActions.get_user(path_params)


@router.post("/users", response_model=(list[ClientUserModelDB] | ClientUserModelDB))
async def create_user(users: (list[dict] | dict), path_params: dict = Depends(path_params)):
	if isinstance(users, list):
		for user in users:
			user = await ClientUserActions.create_client_user(user, path_params)
	else:
		users = await ClientUserActions.create_client_user(users, path_params)
	return users


@router.put("/users/{user_uuid}", response_model=ClientUserModelDB)
async def update_user(user_updates: ClientUserUpdate, path_params: dict = Depends(path_params)):
	return await ClientUserActions.update_user(path_params, user_updates)


@router.delete("/users/{user_uuid}")
async def delete_user(path_params: dict = Depends(path_params)):
	return await ClientUserActions.delete_user(path_params)
