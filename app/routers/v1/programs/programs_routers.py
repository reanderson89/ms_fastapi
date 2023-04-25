from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
from app.models.programs import ProgramModel, ProgramUpdate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Programs"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/programs/", response_model=List[ProgramModel])
async def get_programs(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	programs = session.exec(
		select(ProgramModel).where(
			ProgramModel.client_uuid == client_uuid
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(programs)
	return programs

@router.get("/programs/{program_9char}", response_model=ProgramModel)
async def get_program(
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
	ExceptionHandling.check404(program)
	return program

@router.post("/programs/", response_model=(List[ProgramModel] | ProgramModel))
async def create_program(programs: (List[ProgramModel] | ProgramModel)):
	return CommonRoutes.create_one_or_many(programs)

@router.put("/programs/{program_9char}", response_model=ProgramModel)
async def update_program(
	client_uuid: str,
	program_9char: str,
	program_updates: ProgramUpdate,
	session: Session = Depends(get_session)
):
	program = session.exec(
		select(ProgramModel)
		.where(
			ProgramModel.program_9char == program_9char,
			ProgramModel.client_uuid == client_uuid
		)
	).one_or_none()
	ExceptionHandling.check404(program)
	update_program = program_updates.dict(exclude_unset=True)
	for k, v in update_program.items():
		setattr(program, k, v)
	program.time_updated = int(time())
	session.add(program)
	session.commit()
	session.refresh(program)
	return program

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
	ExceptionHandling.check404(program)
	session.delete(program)
	session.commit()
	return {"ok": True, "Deleted": program}
