from typing import List
from time import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import crud
from .models import Client as ClientModel
from .schema import Client, ClientCreate, ClientUpdate

router = APIRouter()

def check_db():
	# crud.get_db()
	from src.app import SessionLocal
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@router.get("/", response_model=List[Client])
def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(check_db)):
	clients = crud.get_all(db, ClientModel, skip, limit)
	return clients

@router.get("/{client_uuid}", response_model=Client)
def get_client_by_uuid(client_uuid: str, db: Session = Depends(check_db)):
	client = crud.get_by_uuid(db, ClientModel, client_uuid)
	if client is None:
		raise HTTPException(status_code=404, detail="Client not found")
	return client

@router.post("/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(check_db)):
    return crud.create(db, ClientModel, client)

@router.put("/{client_uuid}", response_model=Client)
def update_client_by_uuid(
	client_uuid: str, client_update: ClientUpdate, db: Session = Depends(check_db)
):
	client = crud.update(db, ClientModel, client_uuid, client_update)
	if client is None:
		raise HTTPException(status_code=404, detail="Client not found")
	return client
