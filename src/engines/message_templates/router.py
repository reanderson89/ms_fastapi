from fastapi import APIRouter

router = APIRouter()

@router.get("/messages")
async def get_messages():
	return {"message": "Got all messages"}

@router.get("/messages/{message_template_id}")
async def get_message(message_template_id: int):
	return {"message": f"Got messages for {message_template_id}"}

@router.post("/messages")
async def create_message():
	return {"message": "Created message"}

@router.put("/messages/{message_template_id}")
async def update_message(message_template_id: int):
	return {"message": f"Updated message for {message_template_id}"}

@router.delete("/messages/{message_template_id}")
async def delete_message(message_template_id: int):
	return {"message": f"Deleted message for {message_template_id}"}
