from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
from app.models.programs.admins import ProgramAdminModel, ProgramAdminUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Admins"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/admins", response_model=List[ProgramAdminModel])
async def get_admins(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	admins = session.exec(
		select(ProgramAdminModel).where(
			ProgramAdminModel.client_uuid == client_uuid,
			ProgramAdminModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(admins)
	return admins

@router.get("/admins/{user_uuid}", response_model=ProgramAdminModel)
async def get_admin(
	client_uuid: str,
	program_9char: str,
	user_uuid: str,
	session: Session = Depends(get_session)
):
	admin = session.exec(
		select(ProgramAdminModel)
		.where(
			ProgramAdminModel.user_uuid == user_uuid,
			ProgramAdminModel.client_uuid == client_uuid,
			ProgramAdminModel.program_9char == program_9char
		)
	).one_or_none()
	ExceptionHandling.check404(admin)
	return admin

@router.post("/admins", response_model=(List[ProgramAdminModel] | ProgramAdminModel))
async def create_admin(admins: (List[ProgramAdminModel] | ProgramAdminModel)):
	return CommonRoutes.create_one_or_many(admins)

@router.put("/admins/{user_uuid}", response_model=ProgramAdminModel)
async def update_admin(
	client_uuid: str,
	program_9char: str,
	user_uuid: str,
	admin_updates: ProgramAdminUpdate,
	session: Session = Depends(get_session)
):
	admin = session.exec(
		select(ProgramAdminModel)
		.where(
			ProgramAdminModel.user_uuid == user_uuid,
			ProgramAdminModel.client_uuid == client_uuid,
			ProgramAdminModel.program_9char == program_9char
		)
	).one_or_none()
	ExceptionHandling.check404(admin)
	admin_updates_dict = admin_updates.dict(exclude_unset=True)
	for k, v in admin_updates_dict.items():
		setattr(admin, k, v)
	admin.time_updated = int(time())
	session.add(admin)
	session.commit()
	session.refresh(admin)
	return admin

@router.delete("/admins/{user_uuid}")
async def delete_admin(
	client_uuid: str,
	program_9char: str,
	user_uuid: str,
	session: Session = Depends(get_session)
):
	admin = session.exec(
		select(ProgramAdminModel)
		.where(
			ProgramAdminModel.user_uuid == user_uuid,
			ProgramAdminModel.client_uuid == client_uuid,
			ProgramAdminModel.program_9char == program_9char
		)
	).one_or_none()
	ExceptionHandling.check404(admin)
	session.delete(admin)
	session.commit()
	return {"ok": True, "Deleted:": admin}
