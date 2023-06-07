from fastapi import APIRouter, Depends
from app.models.messages import MessageModel, MessageCreate, MessageUpdate
from app.actions.messages.message_actions import MessageActions
from app.routers.v1.dependencies import get_query_params

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Messages"])


def path_params(client_uuid: str, program_9char: str, message_9char: str=None):
	return {"client_uuid": client_uuid, "program_9char": program_9char, "message_9char": message_9char}


@router.get("/messages", response_model=list[MessageModel])
async def get_messages(
	query_params: dict = Depends(get_query_params),
	path_params: dict = Depends(path_params)
):
	return await MessageActions.get_all(path_params, query_params)


@router.get("/messages/{message_9char}", response_model=MessageModel)
async def get_message(
	path_params: dict = Depends(path_params)
):
	return await MessageActions.get_one(path_params)


@router.post("/messages", response_model=MessageModel)
async def create_message(
	new_message_obj: MessageCreate,
	path_params: dict = Depends(path_params),
	program_uuid: str = Depends(MessageActions.get_program_uuid)
):
	return await MessageActions.create_message(new_message_obj, path_params, program_uuid)


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


@router.put("/messages/{message_9char}", response_model=MessageModel)
async def update_message(
	message_updates: MessageUpdate,
	path_params: dict = Depends(path_params)
):
	return await MessageActions.update_message(path_params, message_updates)


@router.delete("/messages/{message_9char}")
async def delete_message(
	path_params: dict = Depends(path_params)
):
	return await MessageActions.delete_message(path_params)
