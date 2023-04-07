from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/programs/{program_id}/messages")
async def get_messages():
	return {"message": "Got all messages"}

@router.get("/clients/{client_id}/programs/{program_id}/messages/{message_id}")
async def get_message(message_id: int):
	return {"message": f"Got messages for {message_id}"}

@router.post("/clients/{client_id}/programs/{program_id}/messages")
async def create_message():
	return {"message": "Created message"}

# the endpoint might needs to be different for this not to conflict with create_message()
# @router.post("/clients/{client_id}/programs/{program_id}/messages/{message_id}/template") # possible solution
@router.post("/clients/{client_id}/programs/{program_id}/messages/{message_id}") # endpoint in specs
async def create_message_from_template(message_id: int):
	return {"message": f"Created message from template for {message_id}"}

@router.post("/clients/{client_id}/programs/{program_id}/messages/{message_id}/test")
async def test_message(message_id: int):
	return {"message": f"Tested message for {message_id}"}

# send message to program audience
@router.post("/clients/{client_id}/programs/{program_id}/messages/{message_id}/send")
async def send_message(message_id: int):
	return {"message": f"Sent message for {message_id}"}

@router.put("/clients/{client_id}/programs/{program_id}/messages/{message_id}")
async def update_message(message_id: int):
	return {"message": f"Updated message for {message_id}"}

@router.delete("/clients/{client_id}/programs/{program_id}/messages/{message_id}")
async def delete_message(message_id: int):
	return {"message": f"Deleted message for {message_id}"}
