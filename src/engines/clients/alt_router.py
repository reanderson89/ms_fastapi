from typing import List
from time import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import Client as ClientModel
from .schema import Client, ClientCreate, ClientUpdate

router = APIRouter()

def get_db():
	from src.app import SessionLocal
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@router.get("/", response_model=List[Client])
def get_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
	clients = db.query(ClientModel).offset(skip).limit(limit).all()
	return clients

@router.get("/{client_uuid}", response_model=Client)
def get_client_by_uuid(client_uuid: str, db: Session = Depends(get_db)):
	client = db.query(ClientModel).filter(ClientModel.uuid == client_uuid).first()
	if client is None:
		raise HTTPException(status_code=404, detail="Client not found")
	return client

@router.post("/", response_model=Client)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
	new_client = ClientModel(**client.dict())
	db.add(new_client)
	db.commit()
	db.refresh(new_client)
	return new_client

@router.put("/{client_uuid}", response_model=Client)
def update_client_by_uuid(
	client_uuid: str, client_update: ClientUpdate, db: Session = Depends(get_db)
):
	client = db.query(ClientModel).filter(ClientModel.uuid == client_uuid).first()
	if client is None:
		raise HTTPException(status_code=404, detail="Client not found")

	updated_fields = client_update.dict(exclude_unset=True)
	for key, value in updated_fields.items():
		setattr(client, key, value)

	client.time_updated = int(time())
	db.commit()
	db.refresh(client)
	return client
