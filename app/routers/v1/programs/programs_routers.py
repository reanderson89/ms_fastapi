from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
# from app.models.programs import ProgramModel, ProgramUpdate
from app.models.programs.programs_models import ProgramModel, ProgramUpdate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Programs"])

async def get_session():
	async with Session(engine) as session:
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
async def get_program(program_9char: str):
	return CommonRoutes.get_one(ProgramModel, program_9char)

@router.post("/programs/", response_model=ProgramModel)
async def create_program(programs: (ProgramModel | List[ProgramModel])):
	return CommonRoutes.create_one_or_many(programs)

@router.put("/programs/{program_9char}", response_model=ProgramModel)
async def update_program(program_9char: str, program_updates: ProgramUpdate):
	return CommonRoutes.update_one(program_9char, ProgramModel, program_updates)

# should only work if there are no segments or events associated with the program
@router.delete("/programs/{program_9char}")
async def delete_program(program_9char: str):
	return CommonRoutes.delete_one(program_9char, ProgramModel)
