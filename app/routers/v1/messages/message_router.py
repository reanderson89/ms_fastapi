from time import time
from sqlalchemy import select
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.messages import MessageModel, MessageUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Messages"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/messages", response_model=list[MessageModel])
async def get_messages(
	client_uuid: str,
	program_9char: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	messages = session.scalars(
		select(MessageModel).where(
			MessageModel.client_uuid == client_uuid,
			MessageModel.program_9char == program_9char
		)
		.offset(offset)
		.limit(limit)
		).all()
	await ExceptionHandling.check404(messages)
	return messages

@router.get("/messages/{message_9char}", response_model=MessageModel)
async def get_message(
	client_uuid: str,
	program_9char: str,
	message_9char: str,
	session: Session = Depends(get_session)
):
	message = session.scalars(
		select(MessageModel).where(
			MessageModel.client_uuid == client_uuid,
			MessageModel.program_9char == program_9char,
			MessageModel.message_9char == message_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(message)
	return message

@router.post("/messages", response_model=(list[MessageModel] | MessageModel))
async def create_message(message: (list[MessageModel] | MessageModel)):
	return await CommonRoutes.create_one_or_many(message)

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
async def update_message(
	client_uuid: str,
	program_9char: str,
	message_9char: str,
	message_updates: MessageUpdate,
	session: Session = Depends(get_session)
):
	message = session.scalars(
		select(MessageModel)
		.where(
			MessageModel.client_uuid == client_uuid,
			MessageModel.program_9char == program_9char,
			MessageModel.message_9char == message_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(message)
	update_message = message_updates.dict(exclude_unset=True)
	for k, v in update_message.items():
		setattr(message, k, v)
	message.time_updated = int(time())
	session.add(message)
	session.commit()
	session.refresh(message)
	return message

@router.delete("/messages/{message_9char}")
async def delete_message(
	client_uuid: str,
	program_9char: str,
	message_9char: str,
	session: Session = Depends(get_session)
):
	message = session.scalars(
		select(MessageModel)
		.where(
			MessageModel.client_uuid == client_uuid,
			MessageModel.program_9char == program_9char,
			MessageModel.message_9char == message_9char
		)
	).one_or_none()
	await ExceptionHandling.check404(message)
	session.delete(message)
	session.commit()
	return {'ok': True, 'Deleted:': message}