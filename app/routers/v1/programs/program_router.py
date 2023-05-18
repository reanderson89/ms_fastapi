from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
from app.models.programs import ProgramModel, ProgramUpdate
from app.actions.programs.program_actions import ProgramActions

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Programs"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/programs/", response_model=List[ProgramModel])
async def get_programs(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100)
):
	return await ProgramActions.get_by_client_uuid(client_uuid, offset, limit)

@router.get("/programs/{program_9char}", response_model=ProgramModel)
async def get_program(
	client_uuid: str,
	program_9char: str
):
	return await ProgramActions.get_by_program_9char(client_uuid, program_9char)


@router.post("/programs/", response_model_by_alias=True)
async def create_program(
		programs: (List[ProgramModel] | ProgramModel),
		client_uuid: str
):
	return await ProgramActions.create_program_handler(programs, client_uuid)

@router.put("/programs/{program_9char}", response_model=ProgramModel)
async def update_program(
	client_uuid: str,
	program_9char: str,
	program_updates: ProgramUpdate
):
	return await ProgramActions.update_program(client_uuid, program_9char, program_updates)

# should only work if there are no segments or events associated with the program
@router.delete("/programs/{program_9char}")
async def delete_program(
	client_uuid: str,
	program_9char: str,
	session: Session = Depends(get_session)
):
	program = session.exec(
		select(ProgramModel)
		.where(
			ProgramModel.program_9char == program_9char,
			ProgramModel.client_uuid == client_uuid
		)
	).one_or_none()
	await ExceptionHandling.check404(program)
	session.delete(program)
	session.commit()
	return {"ok": True, "Deleted": program}
