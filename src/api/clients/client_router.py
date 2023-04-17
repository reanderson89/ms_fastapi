from typing import List
from time import time
from fastapi import APIRouter
from .client_models import Client, ClientUpdate
from api import CommonRoutes

router = APIRouter()

@router.get("/", response_model=List[Client])
async def get_clients():
	return CommonRoutes.get_all(Client)

@router.get("/{client_uuid}", response_model=Client)
async def get_client_by_uuid(client_uuid: str):
	return CommonRoutes.get_one(Client, client_uuid)

@router.post("/", response_model=Client)
async def create_client(client: (Client|List[Client])):
    return CommonRoutes.create_one_or_many(client)

@router.put("/{client_uuid}", response_model=Client)
async def update_client_by_uuid(client_uuid: str, client_update: ClientUpdate):
	return CommonRoutes.update_one(client_uuid, Client, ClientUpdate)

@router.delete("/{client_uuid}")
async def delete_client_by_uuid(client_uuid: str):
	return CommonRoutes.delete_one(client_uuid, Client)
