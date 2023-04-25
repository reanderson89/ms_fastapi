from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments import SegmentModel, SegmentUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Segments"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/segments", response_model=List[SegmentModel])
async def get_segments(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	segments = session.exec(
		select(SegmentModel).where(
			SegmentModel.client_uuid == client_uuid,
			SegmentModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(segments)
	return segments

@router.get("/segments/{segment_9char}", response_model=SegmentModel)
async def get_segment(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	session: Session = Depends(get_session)
):
	segment = session.exec(
		select(SegmentModel)
		.where(
			SegmentModel.segment_9char == segment_9char,
			SegmentModel.client_uuid == client_uuid,
			SegmentModel.program_9char == program_9char
		)
	).one_or_none()
	ExceptionHandling.check404(segment)
	return segment

@router.post("/segments", response_model=(List[SegmentModel] | SegmentModel))
async def create_segment(segment: (List[SegmentModel] | SegmentModel)):
	return CommonRoutes.create_one_or_many(segment)

@router.put("/segments/{segment_9char}", response_model=SegmentModel)
async def update_segment(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	segment_updates: SegmentUpdate,
	session: Session = Depends(get_session)
):
	segment = session.exec(
		select(SegmentModel)
		.where(
			SegmentModel.segment_9char == segment_9char,
			SegmentModel.client_uuid == client_uuid,
			SegmentModel.program_9char == program_9char
		)
	).one_or_none()
	ExceptionHandling.check404(segment)
	update_segment = segment_updates.dict(exclude_unset=True)
	for k, v in update_segment.items():
		setattr(segment, k, v)
	segment.time_updated = int(time())
	session.add(segment)
	session.commit()
	session.refresh(segment)
	return segment

@router.delete("/segments/{segment_9char}")
async def delete_segment(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	session: Session = Depends(get_session)
):
	segment = session.exec(
		select(SegmentModel)
		.where(
			SegmentModel.segment_9char == segment_9char,
			SegmentModel.client_uuid == client_uuid,
			SegmentModel.program_9char == program_9char
		)
	).one_or_none()
	ExceptionHandling.check404(segment)
	session.delete(segment)
	session.commit()
	return {"ok": True, "Deleted:": segment}
