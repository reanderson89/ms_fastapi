from time import time
from typing import List
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from src.database.config import engine
from .segment_award_models import Award, CreateAward, UpdateAward

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}/awards", response_model=List[Award])
async def get_awards(
	# client_uuid: str,
	program_7char: str,
	segment_7char: str,
):
	with Session(engine) as session:
		awards = session.exec(
			select(Award).where(
				# Award.client_uuid == client_uuid,
				Award.program_7char == program_7char,
				Award.segment_7char == segment_7char,
			)
		).all()
		return awards

@router.get("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}/awards/{uuid}", response_model=Award)
async def get_award(
	# client_uuid: str,
	program_7char: str,
	segment_7char: str,
	uuid: str,
):
	with Session(engine) as session:
		statement = select(Award).where(Award.uuid == uuid)
		award = session.exec(statement).one()
		if not award:
			raise HTTPException(status_code=404, detail="Award not found")
		return award

@router.post("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}/awards", response_model=Award)
async def create_award(
	# client_uuid: str,
	program_7char: str,
	segment_7char: str,
	award: CreateAward,
):
	with Session(engine) as session:
		award_db = Award(**award.dict(), program_7char=program_7char, segment_7char=segment_7char)
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

@router.put("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}/awards/{award_7char}", response_model=Award)
async def update_award(
	# client_uuid: str,
	program_7char: str,
	segment_7char: str,
	award_7char: str,
	award_update: UpdateAward,
):
	with Session(engine) as session:
		statement = select(Award).where(
			Award.award_7char == award_7char,
			Award.program_7char == program_7char,
			Award.segment_7char == segment_7char
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

@router.delete("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}/awards/{award_7char}")
async def delete_award(
	# client_uuid: str,
	program_7char: str,
	segment_7char: str,
	award_7char: str,
):
	with Session(engine) as session:
		statement = select(Award).where(
			Award.award_7char == award_7char,
			Award.program_7char == program_7char,
			Award.segment_7char == segment_7char
		)
		award_db = session.exec(statement).one()
		if not award_db:
			raise HTTPException(status_code=404, detail="Award not found")
		session.delete(award_db)
		session.commit()
		return {'Deleted:': award_db}
