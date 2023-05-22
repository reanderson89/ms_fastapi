from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.programs import ProgramEventModel, ProgramEventUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Events"])

def get_session():
	with Session(engine) as session:
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
	await ExceptionHandling.check404(events)
	return events

@router.get("/events/{event_9char}", response_model=ProgramEventModel)
async def get_event(
	client_uuid: str,
	program_9char: str,
	event_9char: str,
	session: Session = Depends(get_session)
):
	event = session.exec(
		select(ProgramEventModel)
		.where(
			ProgramEventModel.event_9char == event_9char,
			ProgramEventModel.client_uuid == client_uuid,
			ProgramEventModel.program_9char == program_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(event)
	return event

@router.post("/events", response_model=(List[ProgramEventModel] | ProgramEventModel))
async def create_event(events: (List[ProgramEventModel] | ProgramEventModel)):
	return await CommonRoutes.create_one_or_many(events)

@router.put("/events/{event_9char}", response_model=ProgramEventModel)
async def update_event(
	client_uuid: str,
	program_9char: str,
	event_9char: str,
	event_updates: ProgramEventUpdate,
	session: Session = Depends(get_session)
):
	event = session.exec(
		select(ProgramEventModel)
		.where(
			ProgramEventModel.event_9char == event_9char,
			ProgramEventModel.client_uuid == client_uuid,
			ProgramEventModel.program_9char == program_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(event)
	update_event = event_updates.dict(exclude_unset=True)
	for k, v in update_event.items():
		setattr(event, k, v)
	event.time_updated = int(time())
	session.add(event)
	session.commit()
	session.refresh(event)
	return event


# not in endpoint specs
@router.delete("/events/{event_9char}")
async def delete_event(
	client_uuid: str,
	program_9char: str,
	event_9char: str,
	session: Session = Depends(get_session)
):
	event = session.exec(
		select(ProgramEventModel)
		.where(
			ProgramEventModel.event_9char == event_9char,
			ProgramEventModel.client_uuid == client_uuid,
			ProgramEventModel.program_9char == program_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(event)
	session.delete(event)
	session.commit()
	return {"ok": True, "Deleted:": event}
