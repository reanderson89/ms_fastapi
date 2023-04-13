from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_7char}/messages")
async def get_messages():
	return {"message": "Got all messages"}

@router.get("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
async def get_message(message_7char: str):
	return {"message": f"Got messages for {message_7char}"}

@router.post("/clients/{client_uuid}/programs/{program_7char}/messages")
async def create_message():
	return {"message": "Created message"}

# the endpoint might needs to be different for this not to conflict with create_message()
# @router.post("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}/template") # possible solution
@router.post("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}") # endpoint in specs
async def create_message_from_template(message_7char: str):
	return {"message": f"Created message from template for {message_7char}"}

@router.post("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}/test")
async def test_message(message_7char: str):
	return {"message": f"Tested message for {message_7char}"}

# send message to program audience
@router.post("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}/send")
async def send_message(message_7char: str):
	return {"message": f"Sent message for {message_7char}"}

@router.put("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
async def update_message(message_7char: str):
	return {"message": f"Updated message for {message_7char}"}

@router.delete("/clients/{client_uuid}/programs/{program_7char}/messages/{message_7char}")
async def delete_message(message_7char: str):
	return {"message": f"Deleted message for {message_7char}"}
