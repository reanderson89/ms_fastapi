from time import time
from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from src.database.config import engine
from .segment_award_models import Award, UpdateAward

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["segment awards"])

@router.get("/awards", response_model=List[Award])
async def get_awards(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
):
	with Session(engine) as session:
		awards = session.exec(
			select(Award).where(
				# Award.client_uuid == client_uuid,
				Award.program_9char == program_9char,
				Award.segment_9char == segment_9char,
			)
		).all()
		return awards

@router.get("/awards/{uuid}", response_model=Award)
async def get_award(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
	uuid: str,
):
	with Session(engine) as session:
		statement = select(Award).where(Award.uuid == uuid)
		award = session.exec(statement).one()
		if not award:
			raise HTTPException(status_code=404, detail="Award not found")
		return award

@router.post("/awards", response_model=Award)
async def create_award(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award: Award,
):
	with Session(engine) as session:
		award_db = Award(**award.dict(), program_9char=program_9char, segment_9char=segment_9char)
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

@router.put("/awards/{award_9char}", response_model=Award)
async def update_award(
	# client_uuid: str,
	program_9char: str,
	segment_9char: str,
	award_9char: str,
	award_update: UpdateAward,
):
	with Session(engine) as session:
		statement = select(Award).where(
			Award.award_9char == award_9char,
			Award.program_9char == program_9char,
			Award.segment_9char == segment_9char
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
		statement = select(Award).where(
			Award.award_9char == award_9char,
			Award.program_9char == program_9char,
			Award.segment_9char == segment_9char
		)
		award_db = session.exec(statement).one()
		if not award_db:
			raise HTTPException(status_code=404, detail="Award not found")
		session.delete(award_db)
		session.commit()
		return {'Deleted:': award_db}
