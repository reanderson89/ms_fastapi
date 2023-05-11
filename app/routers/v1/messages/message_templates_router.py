from typing import List
from fastapi import APIRouter
from app.routers.v1.v1CommonRouting import CommonRoutes
from app.models.messages import MessageTemplateModel, MessageTemplateUpdateModel

router = APIRouter(tags=["Message Templates"])

@router.get("/messages", response_model=List[MessageTemplateModel])
async def get_message_templates():
    return await CommonRoutes.get_all(MessageTemplateModel)

@router.get("/messages/{message_template_uuid}", response_model=MessageTemplateModel)
async def get_message_template(message_template_uuid: str):
    return await CommonRoutes.get_one(MessageTemplateModel, message_template_uuid)

@router.post("/messages", response_model=(List[MessageTemplateModel] | MessageTemplateModel))
async def create_message_template(templates: (List[MessageTemplateModel] | MessageTemplateModel)):
    return await CommonRoutes.create_one_or_many(templates)

@router.put("/messages/{message_template_uuid}", response_model=MessageTemplateModel)
async def update_message_template(message_template_uuid: str, template_updates: MessageTemplateUpdateModel):
    return await CommonRoutes.update_one(message_template_uuid, MessageTemplateModel, template_updates)

@router.delete("/messages/{message_template_uuid}")
async def delete_template(message_template_uuid: str):
    #TODO: add check for program_messages associated with {message_template_uuid}
    return await CommonRoutes.delete_one(message_template_uuid, MessageTemplateModel)
