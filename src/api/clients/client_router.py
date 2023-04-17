from typing import List
from time import time
from fastapi import APIRouter
from .client_models import ClientModel, ClientUpdate
from src.api import CommonRoutes

router = APIRouter()

@router.get("/", response_model=List[ClientModel])
async def get_clients():
    return CommonRoutes.get_all(ClientModel)

@router.get("/{client_uuid}", response_model=ClientModel)
async def get_client_by_uuid(client_uuid: str):
    return CommonRoutes.get_one(ClientModel, client_uuid)

@router.post("/", response_model=ClientModel)
async def create_client(client: (ClientModel|List[ClientModel])):
    return CommonRoutes.create_one_or_many(client)

@router.put("/{client_uuid}", response_model=ClientModel)
async def update_client_by_uuid(client_uuid: str, client_update: ClientUpdate):
    return CommonRoutes.update_one(client_uuid, ClientModel, ClientUpdate)

@router.delete("/{client_uuid}")
async def delete_client_by_uuid(client_uuid: str):
    return CommonRoutes.delete_one(client_uuid, ClientModel)
