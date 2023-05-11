from sqlmodel import Session, select
from datetime import datetime, timezone
from app.database.config import engine
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.utilities import SHA224Hash
from app.actions.commonActions import CommonActions
from app.actions.clients import ClientActions
from app.models.clients import ClientBudgetModel
from typing import List

class ClientBudgetActions():

	@staticmethod
	async def default_budget_name(client_uuid):
		client_name = await ClientActions.get_name_by_uuid(client_uuid)
		budgetCreationTime = datetime.now(timezone.utc).strftime('%m/%d/%Y %H:%M:%S %Z')
		return f"New {client_name} Budget (created: {budgetCreationTime})"
	
	@staticmethod
	async def check_for_existing_budget_by_name(budget, client_uuid):
		with Session(engine) as session:
			existingBudget = session.exec(
				select(ClientBudgetModel)
				.where(
					ClientBudgetModel.name == budget.name, 
					ClientBudgetModel.client_uuid == client_uuid
				)).one_or_none()
		if existingBudget:
			message = f"A budget with name '{budget.name}' already exists."
			await ExceptionHandling.custom500(message)

	@staticmethod
	async def get_all_budgets(client_uuid: str, session: Session):
		budgets = session.exec(
			select(ClientBudgetModel)
			.where(ClientBudgetModel.client_uuid == client_uuid)
		).all()
		await ExceptionHandling.check404(budgets)
		return budgets
	
	@staticmethod
	async def get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, session: Session | None = None):
		if not session:
			session = Session(engine)
		return session.exec(
			select(ClientBudgetModel)
			.where(ClientBudgetModel.budget_9char == budget_9char,
					ClientBudgetModel.client_uuid == client_uuid)
		).one_or_none()
	
	@staticmethod
	async def get_sub_budgets(budget_9char, client_uuid, session):
		return session.exec(
			select(ClientBudgetModel)
			.where(ClientBudgetModel.client_uuid == client_uuid,
					ClientBudgetModel.parent_9char == budget_9char)
		).all()
	
	@classmethod
	async def check_for_valid_parent(cls, parent_9char, client_uuid):
		parent = await cls.get_budget_by_9char_and_client_uuid(parent_9char, client_uuid)
		if not parent:
			return await ExceptionHandling.custom500("No parent budget with specified 9char has been found.")

	@classmethod
	async def get_one_budget(cls, budget_9char: str, client_uuid: str, session: Session):
		budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, session)
		await ExceptionHandling.check404(budget)
		return budget
	
	@classmethod
	async def create_budget(cls, new_budget, client_uuid: str):
		if new_budget.name:
			await cls.check_for_existing_budget_by_name(new_budget, client_uuid)
		else:
			new_budget.name = await cls.default_budget_name(client_uuid)
		
		if new_budget.parent_9char:
			await cls.check_for_valid_parent(new_budget.parent_9char, client_uuid)
			
		budget = ClientBudgetModel(
			**new_budget.dict(),
			uuid= SHA224Hash(),
			client_uuid=client_uuid,
		)

		#reason why this isnt part of declaration above: https://stackoverflow.com/questions/18950054/class-method-generates-typeerror-got-multiple-values-for-keyword-argument
		budget.budget_9char = await CommonActions.generate_9char()	
		return await CommonRoutes.create_one_or_many(budget)

	@classmethod
	async def update_budget(cls, budget_updates, budget_9char: str, client_uuid: str, session: Session):
		budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, session)
		await ExceptionHandling.check404(budget)
		if budget_updates.parent_9char:
			if budget_updates.parent_9char == budget_9char:
				return await ExceptionHandling.custom500("Cannot set same value for parent_9char and budget_9char.")
			await cls.check_for_valid_parent(budget_updates.parent_9char, client_uuid)

		update_budget = budget_updates.dict(exclude_unset=True)
		for k,v in update_budget.items():
			setattr(budget, k, v)
		session.add(budget)
		session.commit()
		session.refresh(budget)
		return budget
		
	@classmethod
	async def delete_budget(cls, budget_9char: str, client_uuid: str, session: Session):
		budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, session)
		await ExceptionHandling.check404(budget)
		sub_budget = await cls.get_sub_budgets(budget_9char, client_uuid, session)
		if sub_budget:
			return await ExceptionHandling.custom500(f"Unable to delete budget named: {budget.name}. Budget has sub-budgets attached.")
		session.delete(budget)
		session.commit()
		return {'ok': True, 'Deleted:': budget}
	
	# @classmethod
	# async def create_sub_budget(cls, budgets):
	# 	if budgets is List:
	# 		for budget in budgets:
	# 			budget = await cls.create_budget(budget)
