from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.models.programs import ProgramModel, ProgramCreate, ProgramUpdate
from app.actions.programs.program_actions import ProgramActions

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Programs"])


def path_params(client_uuid: str, program_9char: str=None):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char
	}


@router.get("/programs/", response_model=list[ProgramModel])
async def get_programs(
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(get_query_params)
):
	return await ProgramActions.get_by_client_uuid(path_params, query_params)


@router.get("/programs/{program_9char}", response_model=ProgramModel)
async def get_program(
	path_params: dict = Depends(path_params)
):
	return await ProgramActions.get_by_program_9char(path_params)


@router.post("/programs/", response_model_by_alias=True)
async def create_program(
	programs: (list[ProgramCreate] | ProgramCreate),
	path_params: dict = Depends(path_params)
):
	return await ProgramActions.create_program_handler(programs, path_params)


@router.put("/programs/{program_9char}", response_model=ProgramModel)
async def update_program(
	program_updates: ProgramUpdate,
	path_params: dict = Depends(path_params)
):
	return await ProgramActions.update_program(program_updates, path_params)


# should only work if there are no segments or events associated with the program
@router.delete("/programs/{program_9char}")
async def delete_program(
	path_params: dict = Depends(path_params)
):
	return await ProgramActions.delete_program(path_params)

