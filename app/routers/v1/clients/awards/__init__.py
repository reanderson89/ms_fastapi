from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
from app.models.clients.awards import ClientAwardModel, ClientAwardUpdate

router = APIRouter()

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/clients/{client_uuid}/awards", response_model=List[ClientAwardModel])
async def get_awards(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session),
):
	awards = session.exec(
		select(ClientAwardModel)
		.where(ClientAwardModel.client_uuid == client_uuid)
		.offset(offset)
		.limit(limit)
	).all()
	ExceptionHandling.check404(awards)
	return awards

@router.get("/clients/{client_uuid}/awards/{award_9char}", response_model=ClientAwardModel)
async def get_award(award_9char: str):
	return CommonRoutes.get_one(ClientAwardModel, award_9char)

@router.post("/clients/{client_uuid}/awards", response_model=ClientAwardModel)
async def create_award(awards: (ClientAwardModel | List[ClientAwardModel])):
	return CommonRoutes.create_one_or_many(awards)

@router.put("/clients/{client_uuid}/awards/{award_9char}", response_model=ClientAwardModel)
async def update_award(award_9char: str, award_updates: ClientAwardUpdate):
	return CommonRoutes.update_one(award_9char, ClientAwardModel, award_updates)

# this should only work if there is no programs or segments associated with the award
@router.delete("/clients/{client_uuid}/awards/{award_9char}")
async def delete_award(award_9char: str):
	#TODO: add check for programs
	return CommonRoutes.delete_one(award_9char, ClientAwardModel)
