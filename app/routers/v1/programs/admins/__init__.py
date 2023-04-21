from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.programs.admins import ProgramAdminModel, ProgramAdminUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Admins"])

async def get_session():
	async with Session(engine) as session:
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
async def get_admin(user_uuid: str):
	return CommonRoutes.get_one(ProgramAdminModel, user_uuid)

@router.post("/admins", response_model=ProgramAdminModel)
async def create_admin(admins: (ProgramAdminModel | List[ProgramAdminModel])):
	return CommonRoutes.create_one_or_many(admins)

@router.put("/admins/{user_uuid}", response_model=ProgramAdminModel)
async def update_admin(user_uuid: str, admin_updates: ProgramAdminUpdate):
	return CommonRoutes.update_one(user_uuid, ProgramAdminModel, admin_updates)

@router.delete("/admins/{user_uuid}")
async def delete_admin(user_uuid: str):
	return CommonRoutes.delete_one(user_uuid, ProgramAdminModel)
