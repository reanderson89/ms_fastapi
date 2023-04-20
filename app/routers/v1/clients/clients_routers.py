from typing import List
from time import time
from fastapi import APIRouter
from app.models.clients import ClientModel, ClientUpdate
from app.routers.v1.v1CommonRouting import CommonRoutes

router = APIRouter()

@router.get("/clients/", response_model=List[ClientModel])
async def get_clients():
    return CommonRoutes.get_all(ClientModel)

@router.get("/clients/{client_uuid}", response_model=ClientModel)
async def get_client_by_uuid(client_uuid: str):
    return CommonRoutes.get_one(ClientModel, client_uuid)

@router.post("/clients/", response_model=ClientModel)
async def create_client(client: (ClientModel|List[ClientModel])):
    return CommonRoutes.create_one_or_many(client)

@router.put("/clients/{client_uuid}", response_model=ClientModel)
async def update_client_by_uuid(client_uuid: str, client_update: ClientUpdate):
    return CommonRoutes.update_one(client_uuid, ClientModel, ClientUpdate)

# this should only work if there is nothing else associated with the client
@router.delete("/clients/{client_uuid}")
async def delete_client_by_uuid(client_uuid: str):
	#TODO: add check to see if there is anything else associated with the client
	return CommonRoutes.delete_one(client_uuid, ClientModel)
