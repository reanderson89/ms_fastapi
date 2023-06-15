from typing import Union
from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.models.clients import ClientModel, ClientUpdate, ClientCreate
from app.actions.clients.client_actions import ClientActions

router = APIRouter(tags=["Clients"])


@router.get("/clients", response_model=list[ClientModel])
async def get_clients(
	query_params: dict = Depends(get_query_params)
):
	return await ClientActions.get_all_clients(query_params)


@router.get("/clients/{client_uuid}", response_model=ClientModel)
async def get_client(client_uuid: str):
	return await ClientActions.get_client(client_uuid)


@router.post("/clients", response_model=list[ClientModel]|ClientModel)
async def create_client(
	clients: Union[list[ClientCreate], ClientCreate]
):
	return await ClientActions.create_client_handler(clients)


@router.put("/clients/{client_uuid}", response_model=ClientModel)
async def update_client(
	client_uuid: str,
	client_updates: ClientUpdate
):
	return await ClientActions.update_client(client_uuid, client_updates)


# this should only work if there is nothing else associated with the client
@router.delete("/clients/{client_uuid}")
async def delete_client_by_uuid(client_uuid: str):
	#TODO: add check to see if there is anything else associated with the client
	return await ClientActions.delete_client(client_uuid)
