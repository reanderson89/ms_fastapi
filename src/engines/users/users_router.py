from typing import List
from fastapi import APIRouter
from sqlmodel import Session, select
from src.database.config import engine
from .users_model import UsersModel, UsersUpdate
from time import time

router = APIRouter()

@router.get("/users")
async def get_users():
	with Session(engine) as session:
		users = session.exec(select(UsersModel)).all()
		return users

@router.get("/users/{user_uuid}")
async def get_user(user_uuid: str):
	with Session(engine) as session:
		statement = select(UsersModel).where(UsersModel.uuid == user_uuid)
		user = session.exec(statement)
		return user

@router.post("/users")
async def create_users(users: (UsersModel|List[UsersModel])):
	with Session(engine) as session:
		if isinstance(users, List):
			for user in users:
				session.add(user)
		else:
			session.add(users)
		session.commit()
		session.refresh()
		return users

@router.put("/users/{user_uuid}")
async def update_user(user_uuid: str, users_update: UsersUpdate):
	with Session(engine) as session:
		statement = select(UsersModel).where(UsersModel.uuid == user_uuid)
		user = session.exec(statement).one()
		updated_fields = users_update.dict(exclude_unset=True)
		for key, value in updated_fields.items():
			setattr(user, key, value)
		user.time_updated = int(time( ))
		session.add(user)
		session.commit()
		session.refresh(user)
		return user
	
@router.delete("/users/{user_uuid}")
async def delete_user(user_uuid: str):
	with Session(engine) as session:
		statement = select(UsersModel).where(UsersModel.uuid == user_uuid)
		user = session.exec(statement).one()
		session.delete(user)
		session.commit()
		return {'Deleted:': user}
