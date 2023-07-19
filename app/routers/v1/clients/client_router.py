from typing import Annotated
from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.models.clients import ClientModelDB, ClientUpdate, ClientCreate, ClientModel
from app.actions.clients.client_actions import ClientActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(tags=["Clients"])


@router.get("/clients")
async def get_clients(
	client_uuid: Annotated[str, Depends(Permissions(level="2"))],
	query_params: dict = Depends(default_query_params)
) -> Page[ClientModel]:
	return await ClientActions.get_all_clients(query_params)

@router.get("/clients/{client_uuid}", response_model=ClientModel)
async def get_client(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		client_uuid: str
):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientActions.get_client(client_uuid)


@router.post("/clients", response_model=list[ClientModelDB]|ClientModelDB)
async def create_client(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
	clients: list[ClientCreate] | ClientCreate
):
	return await ClientActions.create_client(clients)


@router.put("/clients/{client_uuid}", response_model=ClientModel)
async def update_client(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
	client_uuid: str,
	client_updates: ClientUpdate
):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientActions.update_client(client_uuid, client_updates)


# this should only work if there is nothing else associated with the client
@router.delete("/clients/{client_uuid}")
async def delete_client_by_uuid(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="2"))],
		client_uuid: str
):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	#TODO: add check to see if there is anything else associated with the client
	return await ClientActions.delete_client(client_uuid)
