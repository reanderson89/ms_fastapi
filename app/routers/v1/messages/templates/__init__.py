from app.models.messages.templates import MessageTemplateModel, MessageTemplateUpdateModel
from app.routers.v1.v1CommonRouting import CommonRoutes
from fastapi import APIRouter
from typing import List

router = APIRouter()

@router.get("/messages")
async def get_message_templates():
    return CommonRoutes.get_all(MessageTemplateModel)

@router.get("/messages/{message_template_uuid}")
async def get_message_template(message_template_uuid: str):
    return CommonRoutes.get_one(MessageTemplateModel, message_template_uuid)

@router.post("/messages")
async def create_message_template(templates: (MessageTemplateModel | List[MessageTemplateModel])):
    return CommonRoutes.create_one_or_many(templates)

@router.put("/messages/{message_template_uuid}")
async def update_message_template(message_template_uuid: str, template_updates: MessageTemplateUpdateModel):
    return CommonRoutes.update_one(message_template_uuid, MessageTemplateModel, template_updates)

@router.delete("/messages/{message_template_uuid}")
async def delete_template(message_template_uuid: str):
    #TODO: add check for program_messages associated with {message_template_uuid}
    return CommonRoutes.delete_one(message_template_uuid, MessageTemplateModel)
