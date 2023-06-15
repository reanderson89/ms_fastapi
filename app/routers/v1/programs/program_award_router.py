from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.actions.programs.awards.program_award_actions import ProgramAwardActions
from app.models.programs import ProgramAwardModel, ProgramAwardCreate, ProgramAwardUpdate, ProgramAwardResponse

router = APIRouter(
	prefix="/clients/{client_uuid}/programs/{program_9char}",
	tags=["Client Program Awards"]
)


def path_params(
	client_uuid: str,
	program_9char: str,
	client_award_9char: str=None,
	program_award_9char: str=None
):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char,
		"client_award_9char": client_award_9char,
		"program_award_9char": program_award_9char
	}


@router.get("/awards", response_model=list[ProgramAwardResponse])
async def get_awards(
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(get_query_params)
):
	return await ProgramAwardActions.get_program_awards(path_params, query_params)


@router.get("/awards/{program_award_9char}", response_model=ProgramAwardResponse)
async def get_award(
	path_params: dict = Depends(path_params)
):
	return await ProgramAwardActions.get_award(path_params)


@router.post("/awards/{client_award_9char}", response_model=list[ProgramAwardResponse] | ProgramAwardResponse)
async def create_award(
	awards: list[ProgramAwardCreate] | ProgramAwardCreate,
	path_params: dict = Depends(path_params),
):
	return await ProgramAwardActions.create_award(path_params, awards)


@router.put("/awards/{program_award_9char}", response_model=ProgramAwardResponse)
async def update_award(
	award_updates: ProgramAwardUpdate,
	path_params: dict = Depends(path_params)
):
	return await ProgramAwardActions.update_award(path_params, award_updates)


# TODO: this should only work if there is no segment awards associated with the award
@router.delete("/awards/{program_award_9char}")
async def delete_award(
	path_params: dict = Depends(path_params)
):
	#TODO: add check for segment awards
	return await ProgramAwardActions.delete_award(path_params)
