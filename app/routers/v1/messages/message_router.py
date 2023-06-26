from fastapi import APIRouter, Depends
from typing import Union
from app.routers.v1.pagination import Page
from app.models.messages import MessageModelDB, MessageCreate, MessageUpdate, MessageModel
from app.actions.messages.message_actions import MessageActions
from app.routers.v1.dependencies import default_query_params

router = APIRouter(tags=["Messages"])

@router.get("/messages")
async def get_messages(query_params: dict = Depends(default_query_params)) -> Page[MessageModel]:
	return await MessageActions.get_all(query_params)


@router.get("/messages/{message_9char}", response_model=MessageModelDB)
async def get_message(message_9char: str):
	return await MessageActions.get_one(message_9char)


@router.post("/messages", response_model=list[MessageModelDB]|MessageModelDB)
async def create_message(new_message_obj: Union[list[MessageCreate], MessageCreate]):
	return await MessageActions.create_message(new_message_obj)


# TODO: Role this functionality into create_message
# only difference is the template_uuid being passed in the body
@router.post("/messages/{message_9char}/template", deprecated=True)
async def create_message_from_template(message_9char: str):
	return {"message": f"Created message from template for {message_9char}"}


@router.post("/messages/{message_9char}/test")
async def test_message(message_9char: str):
	return await MessageActions.send_test_message(message_9char)


# send message to program audience
@router.post("/messages/{message_9char}/send")
async def send_message(message_9char: str):
	return await MessageActions.send_message(message_9char)


@router.put("/messages/{message_9char}", response_model=MessageModelDB)
async def update_message(message_9char: str, message_updates: MessageUpdate):
	return await MessageActions.update_message(message_9char, message_updates)


@router.delete("/messages/{message_9char}")
async def delete_message(message_9char: str):
	return await MessageActions.delete_message(message_9char)
