from time import time
from typing import List
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.segments.awards import SegmentAward, SegmentAwardUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["Client Program Segment Awards"])

@router.get("/awards", response_model=List[SegmentAward])
async def get_awards(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
):
	with Session(engine) as session:
		awards = session.exec(
			select(SegmentAward).where(
				# Award.client_uuid == client_uuid,
				SegmentAward.program_9char == program_9char,
				SegmentAward.segment_9char == segment_9char,
			)
		).all()
		return awards

@router.get("/awards/{uuid}", response_model=SegmentAward)
async def get_award(
	# client_uuid: str,
	# program_9char: str,
	# segment_9char: str,
	uuid: str,
):
	with Session(engine) as session:
		statement = select(SegmentAward).where(SegmentAward.uuid == uuid)
		award = session.exec(statement).one()
		if not award:
			raise HTTPException(status_code=404, detail="Award not found")
		return award

@router.post("/awards", response_model=SegmentAward)
async def create_award(
	# client_uuid: str,
	# program_9char: str,
	# segment_9char: str,
	award: SegmentAward,
):
	with Session(engine) as session:
		award_db = SegmentAward(**award.dict())#, program_9char=program_9char, segment_9char=segment_9char
		try:
			session.add(award_db)
			session.commit()
			session.refresh(award_db)
		except IntegrityError as e:
			session.rollback()
			if "Duplicate entry" in str(e):
				raise HTTPException(status_code=400, detail="Duplicate entry")
			raise e
		return award_db

@router.put("/awards/{award_9char}", response_model=SegmentAward)
async def update_award(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award_9char: str,
	award_update: SegmentAwardUpdate,
):
	with Session(engine) as session:
		statement = select(SegmentAward).where(
			SegmentAward.award_9char == award_9char,
			SegmentAward.program_9char == program_9char,
			SegmentAward.segment_9char == segment_9char
		)
		award_db = session.exec(statement).one()
		if not award_db:
			raise HTTPException(status_code=404, detail="Award not found")
		update_data = award_update.dict(exclude_unset=True)
		for key, value in update_data.items():
			setattr(award_db, key, value)
		if hasattr(award_db, 'update_time'):
			award_db.update_time = int(time.time())
		session.add(award_db)
		session.commit()
		session.refresh(award_db)
		return award_db

@router.delete("/awards/{award_9char}")
async def delete_award(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award_9char: str,
):
	with Session(engine) as session:
		statement = select(SegmentAward).where(
			SegmentAward.award_9char == award_9char,
			SegmentAward.program_9char == program_9char,
			SegmentAward.segment_9char == segment_9char
		)
		award_db = session.exec(statement).one()
		if not award_db:
			raise HTTPException(status_code=404, detail="Award not found")
		session.delete(award_db)
		session.commit()
		return {'Deleted:': award_db}
