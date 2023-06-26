from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.models.programs import ProgramEventModelDB, ProgramEventUpdate, ProgramEventCreate, ProgramEventReturn
from app.actions.programs.events.program_event_actions import ProgramEventActions

router = APIRouter(
	prefix="/clients/{client_uuid}/programs/{program_9char}",
	tags=["Client Program Events"]
)


def path_params(client_uuid: str, program_9char: str, event_9char: str=None):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char,
		"event_9char": event_9char
	}


@router.get("/events")
async def get_events(
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(default_query_params)
) -> Page[ProgramEventReturn]:
	return await ProgramEventActions.get_all_events(path_params, query_params)


@router.get("/events/{event_9char}", response_model=ProgramEventModelDB)
async def get_event(
	path_params: dict = Depends(path_params)
):
	return await ProgramEventActions.get_event(path_params)


@router.post("/events", response_model=(list[ProgramEventModelDB] | ProgramEventModelDB))
async def create_event(
	events: (list[ProgramEventCreate] | ProgramEventCreate),
	path_params: dict = Depends(path_params),
	program_uuid: str = Depends(ProgramEventActions.get_program_uuid)
):
	return await ProgramEventActions.create_event(events, path_params, program_uuid)


@router.put("/events/{event_9char}", response_model=ProgramEventModelDB)
async def update_event(
	event_updates: ProgramEventUpdate,
	path_params: dict = Depends(path_params)
):
	return await ProgramEventActions.update_event(event_updates, path_params)


#TODO: Check, delete is not in endpoint specs doc
@router.delete("/events/{event_9char}")
async def delete_event(
	path_params: dict = Depends(path_params)
):
	return await ProgramEventActions.delete_event(path_params)
