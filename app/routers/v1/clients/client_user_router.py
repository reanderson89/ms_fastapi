from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.models.clients import ClientUserModelDB, ClientUserUpdate, ClientUserModel
from app.actions.clients.user import ClientUserActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Users"])


def path_params(client_uuid: str, user_uuid: str=None):
	return {
		"client_uuid": client_uuid,
		"user_uuid": user_uuid
	}


@router.get("/users")
async def get_users(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	client_uuid: str,
	query_params: dict = Depends(default_query_params)
) -> Page[ClientUserModel]:
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientUserActions.get_all_users(client_uuid, query_params)


@router.get("/users/{user_uuid}", response_model=ClientUserModelDB)
async def get_user(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		client_uuid: str,
		path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientUserActions.get_user(path_params)


@router.post("/users", response_model=(list[ClientUserModelDB] | ClientUserModelDB))
async def create_user(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		users: (list[dict] | dict),
		path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, path_params.get("client_uuid"))
	if isinstance(users, list):
		for user in users:
			user = await ClientUserActions.create_client_user(user, path_params)
	else:
		users = await ClientUserActions.create_client_user(users, path_params)
	return users

@router.put("/users/{user_uuid}", response_model=(dict | ClientUserModel))
async def update_users(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		client_uuid: str,
		user_updates: (list[ClientUserUpdate] | ClientUserUpdate),
		path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	if path_params.get("user_uuid") == "bulk":
		return await ClientUserActions.update_users(path_params, user_updates)
	return await ClientUserActions.update_user(path_params, user_updates)

@router.delete("/users/{user_uuid}")
async def delete_user(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
		client_uuid: str,
		path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientUserActions.delete_user(path_params)
