from typing import List
from fastapi import APIRouter, Query, Depends
from sqlmodel import Session, select
from src.database.config import engine
from src.api import CommonRoutes, ExceptionHandling
from .program_message_model import ProgramMessageModel, ProgramMessageUpdate

router = APIRouter(prefic="/clients/{client_uuid}/programs/{program_9char}", tags=["program messages"])

async def get_session():
	async with Session(engine) as session:
		yield session

@router.get("/messages", response_model=List[ProgramMessageModel])
async def get_messages(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	messages = session.exec(
		select(ProgramMessageModel).where(
			ProgramMessageModel.client_uuid == client_uuid,
			ProgramMessageModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(messages)
	return messages

@router.get("/messages/{message_9char}", response_model=ProgramMessageModel)
async def get_message(message_9char: str):
	return CommonRoutes.get_one(ProgramMessageModel, message_9char)

@router.post("/messages")
async def create_message(message: (ProgramMessageModel | List[ProgramMessageModel])):
	return CommonRoutes.create_one_or_many(message)

# the endpoint might needs to be different for this not to conflict with create_message()
# @router.post("/messages/{message_9char}/template") # possible solution
# TODO
@router.post("/messages/{message_9char}")
async def create_message_from_template(message_9char: str):
	return {"message": f"Created message from template for {message_9char}"}

# TODO
@router.post("/messages/{message_9char}/test")
async def test_message(message_9char: str):
	return {"message": f"Tested message for {message_9char}"}

# TODO
# send message to program audience
@router.post("/messages/{message_9char}/send")
async def send_message(message_9char: str):
	return {"message": f"Sent message for {message_9char}"}

@router.put("/messages/{message_9char}", response_model=ProgramMessageModel)
async def update_message(message_9char: str, message_updates: ProgramMessageUpdate):
	return CommonRoutes.update_one(message_9char, ProgramMessageModel, message_updates)

@router.delete("/messages/{message_9char}")
async def delete_message(message_9char: str):
	return CommonRoutes.delete_one(message_9char, ProgramMessageModel)
