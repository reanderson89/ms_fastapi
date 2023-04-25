from typing import List
from time import time
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
from app.models.clients.awards import ClientAwardModel, ClientAwardUpdate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Awards"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/awards", response_model=List[ClientAwardModel])
async def get_awards(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	awards = session.exec(
		select(ClientAwardModel)
		.where(ClientAwardModel.client_uuid == client_uuid)
		.offset(offset)
		.limit(limit)
	).all()
	ExceptionHandling.check404(awards)
	return awards

@router.get("/awards/{award_9char}", response_model=ClientAwardModel)
async def get_award(
	client_uuid: str,
	award_9char: str,
	session: Session = Depends(get_session),
):
	award = session.exec(
		select(ClientAwardModel)
		.where(ClientAwardModel.award_9char == award_9char,
				ClientAwardModel.client_uuid == client_uuid)
	).one_or_none()
	ExceptionHandling.check404(award)
	return award

@router.post("/awards", response_model=(List[ClientAwardModel] | ClientAwardModel))
async def create_award(awards: (List[ClientAwardModel] | ClientAwardModel)):
	return CommonRoutes.create_one_or_many(awards)

@router.put("/awards/{award_9char}", response_model=ClientAwardModel)
async def update_award(
	client_uuid: str,
	award_9char: str,
	award_updates: ClientAwardUpdate,
	session: Session = Depends(get_session)
):
	award = session.exec(
		select(ClientAwardModel)
		.where(
			ClientAwardModel.award_9char == award_9char,
			ClientAwardModel.client_uuid == client_uuid
		)
	).one_or_none()
	ExceptionHandling.check404(award)
	update_award = award_updates.dict(exclude_unset=True)
	for k,v in update_award.items():
		setattr(award, k, v)
	award.time_updated = int(time())
	session.add(award)
	session.commit()
	session.refresh(award)
	return award
	

# this should only work if there is no programs or segments associated with the award
@router.delete("/awards/{award_9char}")
async def delete_award(award_9char: str, client_uuid: str,
			session: Session = Depends(get_session)):
	#TODO: add check for programs
	award = session.exec(
		select(ClientAwardModel)
		.where(ClientAwardModel.award_9char == award_9char,
				ClientAwardModel.client_uuid == client_uuid)
	).one_or_none()
	ExceptionHandling.check404(award)
	session.delete(award)
	session.commit()
	return {'ok': True, 'Deleted:': award} 
