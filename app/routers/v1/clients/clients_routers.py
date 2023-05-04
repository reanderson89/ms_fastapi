from typing import List, Union
from fastapi import APIRouter
from app.models.clients import ClientModel, ClientUpdate
from app.models.clients.clients_model import ClientExpanded
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.actions.clients.clients_actions import ClientActions

router = APIRouter(tags=["Clients"])

@router.get("/clients/", response_model=List[ClientModel])
async def get_clients():
    return CommonRoutes.get_all(ClientModel)

@router.get("/clients/{client_uuid}", response_model_by_alias=True)
async def get_client_by_uuid(client_uuid: str):
    client = CommonRoutes.get_one(ClientModel, client_uuid)
    response_model = ClientModel
    return response_model.from_orm(client)


@router.post("/clients/", response_model_by_alias=True)
async def create_client(clients: Union[List[ClientModel], ClientModel]):
    client_return = await ClientActions.create_client_handler(clients)
    return client_return

@router.put("/clients/{client_uuid}", response_model=ClientModel)
async def update_client_by_uuid(client_uuid: str, client_update: ClientUpdate):
    return CommonRoutes.update_one(client_uuid, ClientModel, client_update)

# this should only work if there is nothing else associated with the client
@router.delete("/clients/{client_uuid}")
async def delete_client_by_uuid(client_uuid: str):
    #TODO: add check to see if there is anything else associated with the client
    return CommonRoutes.delete_one(client_uuid, ClientModel)
