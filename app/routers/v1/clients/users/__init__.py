from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
from app.models.clients.user import ClientUserModel, ClientUserUpdate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Users"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/users", response_model=List[ClientUserModel])
async def get_users(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
	):
	users = session.exec(
		select(ClientUserModel)
		.where(ClientUserModel.client_uuid == client_uuid)
		.offset(offset)
		.limit(limit)
	).all()
	ExceptionHandling.check404(users)
	return users

@router.get("/users/{user_uuid}", response_model=ClientUserModel)
async def get_user(
	client_uuid: str,
	user_uuid: str,
	session: Session = Depends(get_session)
):
	user = session.exec(
		select(ClientUserModel)
		.where(ClientUserModel.client_uuid == client_uuid,
				ClientUserModel.user_uuid == user_uuid)
	).one_or_none()
	ExceptionHandling.check404(user)
	return user

@router.post("/users", response_model=(List[ClientUserModel] | ClientUserModel))
async def create_user(users: (List[ClientUserModel] | ClientUserModel)):
	return CommonRoutes.create_one_or_many(users)

@router.put("/users/{user_uuid}", response_model=ClientUserModel)
async def update_user(
	client_uuid: str,
	user_uuid: str,
	user_updates: ClientUserUpdate,
	session: Session = Depends(get_session)
):
	user = session.exec(
		select(ClientUserModel)
		.where(ClientUserModel.client_uuid == client_uuid,
				ClientUserModel.user_uuid == user_uuid)
		).one_or_none()
	print(user)
	ExceptionHandling.check404(user)
	update_user = user_updates.dict(exclude_unset=True)
	for key, value in update_user.items():
		setattr(user, key, value)
	user.time_updated = int(time())
	session.add(user)
	session.commit()
	session.refresh(user)
	return user

@router.delete("/users/{user_uuid}")
async def delete_user(
	user_uuid: str,
	client_uuid: str,
	session: Session = Depends(get_session)
):
	user = session.exec(
		select(ClientUserModel)
		.where(ClientUserModel.client_uuid == client_uuid,
				ClientUserModel.user_uuid == user_uuid)
	).one_or_none()
	ExceptionHandling.check404(user)
	session.delete(user)
	session.commit()
	return {"ok": True, "Deleted": user}
