from fastapi import APIRouter

router = APIRouter()

@router.get("/messages")
async def get_msg_templates():
	return {"message": "Got all messages"}

@router.get("/messages/{message_template_uuid}")
async def get_msg_templates(message_template_uuid: int):
	return {"message": f"Got messages for {message_template_uuid}"}

@router.post("/messages")
async def create_msg_templates():
	return {"message": "Created message"}

@router.put("/messages/{message_template_uuid}")
async def update_msg_templates(message_template_uuid: int):
	return {"message": f"Updated message for {message_template_uuid}"}

# this should only work if there is no program_messages associated with the message_template_uuid
@router.delete("/messages/{message_template_uuid}")
async def delete_msg_templates(message_template_uuid: int):
	return {"message": f"Deleted message for {message_template_uuid}"}
