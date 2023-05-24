from fastapi import APIRouter, Depends
from app.models.clients import ClientUserModel, ClientUserUpdate
from app.actions.clients.user import ClientUserActions
from app.actions.helper_actions import HelperActions
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Users"])

@router.get("/users", response_model=list[ClientUserModel])
async def get_users(client_uuid: str, session: Session = Depends(HelperActions.get_session)):
	return await ClientUserActions.getAllUsers(client_uuid, session)

@router.get("/users/{user_uuid}", response_model=ClientUserModel)
async def get_user(client_uuid: str, user_uuid: str, session: Session = Depends(HelperActions.get_session)):
	return await ClientUserActions.getUser(client_uuid, user_uuid, session)

@router.post("/users", response_model=(list[ClientUserModel] | ClientUserModel))
async def create_user(client_uuid: str,	users: (list[dict] | dict), session: Session = Depends(HelperActions.get_session)):
	if users is list:
		for user in users:
			user = await ClientUserActions.createClientUser(user, client_uuid, session)
	else:
		users = await ClientUserActions.createClientUser(users, client_uuid, session)
	return users

@router.put("/users/{user_uuid}", response_model=ClientUserModel)
async def update_user(client_uuid: str, user_uuid: str, user_updates: ClientUserUpdate, session: Session = Depends(HelperActions.get_session)):
	return await ClientUserActions.updateUser(client_uuid, user_uuid, user_updates, session)

@router.delete("/users/{user_uuid}")
async def delete_user(user_uuid: str, client_uuid: str, session: Session = Depends(HelperActions.get_session)):
	return await ClientUserActions.deleteUser(client_uuid, user_uuid, session)
