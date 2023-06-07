from app.actions.base_actions import BaseActions
from app.models.messages import MessageTemplateModel, MessageCreate, MessageTemplateUpdate

class MessageTemplateActions():

	@staticmethod
	async def get_all_templates(query_params: dict):
		return await BaseActions.get_all(
			MessageTemplateModel,
			query_params
		)

	@staticmethod
	async def get_template(template_uuid: str):
		return await BaseActions.get_one_where(
			MessageTemplateModel,
			[MessageTemplateModel.uuid == template_uuid]
		)

	@staticmethod
	async def create_template(template: MessageCreate):
		new_template = MessageTemplateModel(**template.dict())
		return await BaseActions.create(new_template)

	@staticmethod
	async def update_template(template_uuid: str, template_updates: MessageTemplateUpdate):
		return await BaseActions.update(
			MessageTemplateModel,
			[MessageTemplateModel.uuid == template_uuid],
			template_updates
		)

	@staticmethod
	async def delete_template(template_uuid: str):
		return await BaseActions.delete_one(
			MessageTemplateModel,
			[MessageTemplateModel.uuid == template_uuid]
		)
