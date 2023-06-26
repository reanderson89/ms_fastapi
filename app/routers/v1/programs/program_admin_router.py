from typing import Union
from fastapi import APIRouter, Query, Depends
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.models.programs import AdminModelDB, AdminUpdate, AdminCreate, AdminStatus, AdminExpand, AdminModel
from app.actions.programs.admins import ProgramAdminActions

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Admins"])


def path_params(client_uuid: str, program_9char: str, user_uuid: str=None):
	return {"client_uuid": client_uuid, "program_9char": program_9char, "user_uuid": user_uuid}

def query_params(offset: int, limit: int = Query(default=100, lte=100)):
	return {"offset": offset, "limit": limit}

@router.get("/admins")
async def get_admins(
	query_params: dict = Depends(default_query_params),
	path_params: dict = Depends(path_params)
) -> Page[AdminModel]:
	return await ProgramAdminActions.get_program_admins(path_params, query_params)

@router.get("/admins/{user_uuid}", response_model=AdminModelDB)
async def get_admin(
	expand: AdminExpand = None,
	path_params: dict = Depends(path_params)
):
	return await ProgramAdminActions.get_program_admin(path_params)

@router.post("/admins", response_model= Union[AdminStatus, list[AdminStatus]])
async def create_admin(
	path_params: dict = Depends(path_params),
	admins: Union[AdminCreate, list[AdminCreate]] = Depends(ProgramAdminActions.check_existing)
):
	if isinstance(admins, list):
		for admin in admins:
			if isinstance(admin, AdminCreate):
				admin = await ProgramAdminActions.create_program_admin(path_params, admins)
		return admins
	elif isinstance(admins, AdminStatus):
		return admins
	return await ProgramAdminActions.create_program_admin(path_params, admins)

@router.put("/admins/{user_uuid}", response_model=AdminModelDB)
async def update_admin(
	admin_updates: AdminUpdate,
	path_params: dict = Depends(path_params)
):
	return await ProgramAdminActions.update_program_admin(path_params, admin_updates)

@router.delete("/admins/{user_uuid}")
async def delete_admin(
	path_params: dict = Depends(path_params)
):
	return await ProgramAdminActions.delete_program_admin(path_params)
