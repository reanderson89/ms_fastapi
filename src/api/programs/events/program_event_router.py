from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from src.database.config import engine
from src.api import CommonRoutes, ExceptionHandling
from .program_event_models import ProgramEventModel, ProgramEventUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["program events"])

async def get_session():
	async with Session(engine) as session:
		yield session

@router.get("/events", response_model=List[ProgramEventModel])
async def get_events(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	events = session.exec(
		select(ProgramEventModel).where(
			ProgramEventModel.client_uuid == client_uuid,
			ProgramEventModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(events)
	return events

@router.get("/events/{event_9char}", response_model=ProgramEventModel)
async def get_event(event_9char: str):
	return CommonRoutes.get_one(ProgramEventModel, event_9char)

@router.post("/events", response_model=ProgramEventModel)
async def create_event(events: (ProgramEventModel | List[ProgramEventModel])):
	return CommonRoutes.create_one_or_many(events)

@router.put("/events/{event_9char}", response_model=ProgramEventModel)
async def update_event(event_9char: str, event_updates: ProgramEventUpdate):
	return CommonRoutes.update_one(event_9char, ProgramEventModel, event_updates)

# not in endpoint specs
@router.delete("/events/{event_9char}")
async def delete_event(event_9char: str):
	return CommonRoutes.delete_one(event_9char, ProgramEventModel)
