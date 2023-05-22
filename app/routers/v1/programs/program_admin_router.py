from typing import List, Union
from fastapi import APIRouter, Query, Depends
from app.models.programs import AdminModel, AdminUpdate, AdminCreate, AdminStatus, AdminExpand
from app.actions.programs.admins import ProgramAdminActions

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Admins"])


def common_uuids(client_uuid: str, program_9char: str, user_uuid: str=None):
	return {"client_uuid": client_uuid, "program_9char": program_9char, "user_uuid": user_uuid}

def common_args(offset: int, limit: int = Query(default=100, lte=100)):
	return {"offset": offset, "limit": limit}

@router.get("/admins", response_model=List[AdminModel])
async def get_admins(
	args: dict = Depends(common_args),
	ids: dict = Depends(common_uuids)
):
	return await ProgramAdminActions.get_program_admins(ids, args)

@router.get("/admins/{user_uuid}", response_model=AdminModel)
async def get_admin(
	expand: AdminExpand = None,
	ids: dict = Depends(common_uuids)
):
	return await ProgramAdminActions.get_program_admin(ids)

@router.post("/admins", response_model= Union[AdminStatus, List[AdminStatus]])
async def create_admin(
	ids: dict = Depends(common_uuids),
	admins: Union[AdminCreate, List[AdminCreate]] = Depends(ProgramAdminActions.check_existing)
):
	if isinstance(admins, list):
		for admin in admins:
			if isinstance(admin, AdminCreate):
				admin = await ProgramAdminActions.create_program_admin(ids, admins)
		return admins
	elif isinstance(admins, AdminStatus):
		return admins
	return await ProgramAdminActions.create_program_admin(ids, admins)

@router.put("/admins/{user_uuid}", response_model=AdminModel)
async def update_admin(
	admin_updates: AdminUpdate,
	ids: dict = Depends(common_uuids)
):
	return await ProgramAdminActions.update_program_admin(ids, admin_updates)

@router.delete("/admins/{user_uuid}")
async def delete_admin(
	ids: dict = Depends(common_uuids)
):
	return await ProgramAdminActions.delete_program_admin(ids)
