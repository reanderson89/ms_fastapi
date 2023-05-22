from time import time
from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments import SegmentAward, SegmentAwardUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["Client Program Segment Awards"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/awards", response_model=List[SegmentAward])
async def get_awards(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	awards = session.exec(
		select(SegmentAward)
		.where(
			SegmentAward.client_uuid == client_uuid,
			SegmentAward.program_9char == program_9char,
			SegmentAward.segment_9char == segment_9char
		)
		.offset(offset)
		.limit(limit)
	).all()
	await ExceptionHandling.check404(awards)
	return awards

@router.get("/awards/{award_9char}", response_model=SegmentAward)
async def get_award(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award_9char: str,
	session: Session = Depends(get_session)
):
	award = session.exec(
		select(SegmentAward)
		.where(
			SegmentAward.award_9char == award_9char,
			SegmentAward.client_uuid == client_uuid,
			SegmentAward.program_9char == program_9char,
			SegmentAward.segment_9char == segment_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(award)
	return award

@router.post("/awards", response_model=(List[SegmentAward] | SegmentAward))
async def create_award(award: (List[SegmentAward] | SegmentAward)):
	return await CommonRoutes.create_one_or_many(award)

@router.put("/awards/{award_9char}", response_model=SegmentAward)
async def update_award(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award_9char: str,
	award_update: SegmentAwardUpdate,
	session: Session = Depends(get_session)
):
	award = session.exec(
		select(SegmentAward)
		.where(
			SegmentAward.award_9char == award_9char,
			SegmentAward.client_uuid == client_uuid,
			SegmentAward.program_9char == program_9char,
			SegmentAward.segment_9char == segment_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(award)
	update_award = award_update.dict(exclude_unset=True)
	for k, v in update_award.items():
		setattr(award, k, v)
	award.time_updated = int(time())
	session.add(award)
	session.commit()
	session.refresh(award)
	return award

@router.delete("/awards/{award_9char}")
async def delete_award(
	client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award_9char: str,
	session: Session = Depends(get_session)
):
	award = session.exec(
		select(SegmentAward)
		.where(
			SegmentAward.award_9char == award_9char,
			SegmentAward.client_uuid == client_uuid,
			SegmentAward.program_9char == program_9char,
			SegmentAward.segment_9char == segment_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(award)
	session.delete(award)
	session.commit()
	return {"ok": "true", "Deleted": award}
