from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
# from app.models.messages import MessageModel, MessageUpdate
from app.models.messages.message_models import MessageModel, MessageUpdate

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Messages"])

async def get_session():
	async with Session(engine) as session:
		yield session

@router.get("/messages", response_model=List[MessageModel])
async def get_messages(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	messages = session.exec(
		select(MessageModel).where(
			MessageModel.client_uuid == client_uuid,
			MessageModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(messages)
	return messages

@router.get("/messages/{message_9char}", response_model=MessageModel)
async def get_message(message_9char: str):
	return CommonRoutes.get_one(MessageModel, message_9char)

@router.post("/messages")
async def create_message(message: (MessageModel | List[MessageModel])):
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

@router.put("/messages/{message_9char}", response_model=MessageModel)
async def update_message(message_9char: str, message_updates: MessageUpdate):
	return CommonRoutes.update_one(message_9char, MessageModel, message_updates)

@router.delete("/messages/{message_9char}")
async def delete_message(message_9char: str):
	return CommonRoutes.delete_one(message_9char, MessageModel)
