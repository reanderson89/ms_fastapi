from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.models.programs import ProgramModelDB, ProgramCreate, ProgramUpdate, ProgramResponse
from app.actions.programs.program_actions import ProgramActions
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Programs"])


def path_params(client_uuid: str, program_9char: str=None):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char
	}


@router.get("/programs")
async def get_programs(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(default_query_params)
) -> Page[ProgramResponse]:
	await check_jwt_client_with_client(client_uuid_jwt, path_params['client_uuid'])
	return await ProgramActions.get_by_client_uuid(path_params, query_params)


@router.get("/programs/{program_9char}", response_model=ProgramModelDB)
async def get_program(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	path_params: dict = Depends(path_params),
):
	await check_jwt_client_with_client(client_uuid_jwt, path_params['client_uuid'])
	return await ProgramActions.get_by_program_9char(path_params)


@router.post("/programs", response_model_by_alias=True)
async def create_program(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	programs: (list[ProgramCreate] | ProgramCreate),
	path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, path_params['client_uuid'])
	return await ProgramActions.create_program_handler(programs, path_params)


@router.put("/programs/{program_9char}", response_model=ProgramModelDB)
async def update_program(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	program_updates: ProgramUpdate,
	path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, path_params['client_uuid'])
	return await ProgramActions.update_program(program_updates, path_params)


# should only work if there are no segments or events associated with the program
@router.delete("/programs/{program_9char}")
async def delete_program(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	path_params: dict = Depends(path_params)
):
	await check_jwt_client_with_client(client_uuid_jwt, path_params['client_uuid'])
	return await ProgramActions.delete_program(path_params)
