from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_uuid}/messages")
async def get_messages():
	return {"message": "Got all messages"}

@router.get("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}")
async def get_message(message_uuid: str):
	return {"message": f"Got messages for {message_uuid}"}

@router.post("/clients/{client_uuid}/programs/{program_uuid}/messages")
async def create_message():
	return {"message": "Created message"}

# the endpoint might needs to be different for this not to conflict with create_message()
# @router.post("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}/template") # possible solution
@router.post("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}") # endpoint in specs
async def create_message_from_template(message_uuid: str):
	return {"message": f"Created message from template for {message_uuid}"}

@router.post("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}/test")
async def test_message(message_uuid: str):
	return {"message": f"Tested message for {message_uuid}"}

# send message to program audience
@router.post("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}/send")
async def send_message(message_uuid: str):
	return {"message": f"Sent message for {message_uuid}"}

@router.put("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}")
async def update_message(message_uuid: str):
	return {"message": f"Updated message for {message_uuid}"}

@router.delete("/clients/{client_uuid}/programs/{program_uuid}/messages/{message_uuid}")
async def delete_message(message_uuid: str):
	return {"message": f"Deleted message for {message_uuid}"}
