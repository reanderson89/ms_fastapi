from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.actions.messages.templates.template_actions import MessageTemplateActions
from app.models.messages import MessageTemplateModel, MessageTemplateCreate, MessageTemplateUpdate

router = APIRouter(tags=["Message Templates"])


@router.get("/messages", response_model=list[MessageTemplateModel])
async def get_message_templates(
	query_params: dict = Depends(get_query_params)
):
	return await MessageTemplateActions.get_all_templates(query_params)


@router.get("/messages/{message_template_uuid}", response_model=MessageTemplateModel)
async def get_message_template(message_template_uuid: str):
	return await MessageTemplateActions.get_template(message_template_uuid)


@router.post("/messages", response_model=(list[MessageTemplateModel] | MessageTemplateModel))
async def create_message_template(templates: (list[MessageTemplateCreate] | MessageTemplateCreate)):
	return await MessageTemplateActions.create_template(templates)


@router.put("/messages/{message_template_uuid}", response_model=MessageTemplateModel)
async def update_message_template(message_template_uuid: str, template_updates: MessageTemplateUpdate):
	return await MessageTemplateActions.update_template(message_template_uuid, template_updates)


@router.delete("/messages/{message_template_uuid}")
async def delete_template(message_template_uuid: str):
	#TODO: add check for program_messages associated with {message_template_uuid}
	return await MessageTemplateActions.delete_template(message_template_uuid)
