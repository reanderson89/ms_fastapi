from datetime import datetime
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.utilities import SHA224Hash
from app.actions.helper_actions import HelperActions
from app.actions.clients import ClientActions
from app.models.clients import ClientBudgetModel, ClientBudgetExpanded, ClientModel, ClientBudgetShortExpand
from .client_sub_budget_actions import ClientSubBudgetActions

from app.actions.base_actions import BaseActions

class ClientBudgetActions():

	@staticmethod
	async def default_budget_name(client_uuid):
		client_name = await ClientActions.get_client_name(client_uuid)
		budgetCreationTime = datetime.now(datetime.UTC).strftime("%m/%d/%Y %H:%M:%S %Z")
		return f"New {client_name} Budget (created: {budgetCreationTime})"
	
	@staticmethod
	async def check_for_existing_budget_by_name(budget, client_uuid):
		existingBudget = await BaseActions.check_if_exists(ClientBudgetModel, [
			ClientBudgetModel.name == budget.name, 
			ClientBudgetModel.client_uuid == client_uuid
			])
		if existingBudget:
			message = f"A budget with name '{budget.name}' already exists."
			await ExceptionHandling.custom405(message)
		else:
			return budget.name
		
	@staticmethod
	async def get_all_budgets(client_uuid: str):
		budgets = await BaseActions.get_all_where(ClientBudgetModel, [ClientBudgetModel.client_uuid == client_uuid])
		return budgets
	
	@staticmethod #this goes from child --> parent
	async def get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, check404=False):
		return await BaseActions.get_one_where(ClientBudgetModel, [
			ClientBudgetModel.budget_9char == budget_9char,
			ClientBudgetModel.client_uuid == client_uuid
		], check404)

	@staticmethod #this goes from parent --> children
	async def get_budgets_by_parent_9char(budget):
		return await BaseActions.get_all_where(ClientBudgetModel, [
			ClientBudgetModel.parent_9char == budget.budget_9char,
			ClientBudgetModel.client_uuid == budget.client_uuid
		], check404=False)
	
	@staticmethod
	async def get_all_subbudgets_value(subbudgets):
		total = 0
		for budget in subbudgets:
			total += abs(budget.value)
		return total

	@classmethod
	async def validate_new_budget_name(cls, new_budget, client_uuid):
		if new_budget.name:
			return await cls.check_for_existing_budget_by_name(new_budget, client_uuid)
		return await cls.default_budget_name(client_uuid)

	@classmethod
	async def check_for_valid_parent(cls, parent_9char, client_uuid):
		parent = await cls.get_budget_by_9char_and_client_uuid(parent_9char, client_uuid)
		if not parent:
			return await ExceptionHandling.custom405("No parent budget with specified 9char has been found.")
		return parent

	@classmethod
	async def get_one_budget(cls, budget_9char: str, client_uuid: str, expanded):
		budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid, True)
		subbudgets = await cls.get_all_subbudgets(budget)
		client = await CommonRoutes.get_one(ClientModel, client_uuid)
		print("\n\n\n", budget, "\n", client, "\n\n\n")
		if expanded:
			budget = ClientBudgetExpanded.from_orm(budget)
			budget.client = client
			budget.subbudgets_expanded = subbudgets
		else:
			budget = ClientBudgetShortExpand.from_orm(budget)
			value =  await cls.get_all_subbudgets_value(subbudgets)
			budget.subbudgets = {
				"subbudgets": len(subbudgets),
				"value": value
			}
			budget.client = client.name
		return budget

	@classmethod
	async def get_all_subbudgets(cls, budget):
		stack = []
		#get the 1st level of children budgets
		budgets = await cls.get_budgets_by_parent_9char(budget)
		for i in budgets:
			stack.append(i)
		return_budgets = []
		while stack:
			budget = stack.pop()
			budgets = await cls.get_budgets_by_parent_9char(budget)
			for i in budgets:
				stack.append(i) if i else None
			return_budgets.append(budget) if budget else None
		return return_budgets

	@classmethod
	async def create_budget(cls, new_budget, client_uuid: str):
		new_budget.name = await cls.validate_new_budget_name(new_budget, client_uuid)
		if new_budget.budget_type in [1, 2] and new_budget.parent_9char is None:
				return await ExceptionHandling.custom405("A passthrough budget must have a parent budget.")
		elif new_budget.parent_9char:
			parent = await cls.check_for_valid_parent(new_budget.parent_9char, client_uuid)
			return await ClientSubBudgetActions.create_sub_budget(new_budget, parent)
		else:
			budget = ClientBudgetModel(
				**new_budget.dict(),
				uuid= SHA224Hash(),
				client_uuid=client_uuid
			)

			#reason why this isnt part of declaration above: https://stackoverflow.com/questions/18950054/class-method-generates-typeerror-got-multiple-values-for-keyword-argument
			budget.budget_9char = await HelperActions.generate_9char()
			return await CommonRoutes.create_one_or_many(budget)

	@classmethod
	async def update_budget(cls, budget_updates, budget_9char: str, client_uuid: str):
		budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid)
		"""
		add check for:
		if a budget has a program attached, a child, or an expenditure it cannot be modified except for name and value
		"""
		parent_9char = budget_updates.parent_9char if budget_updates.parent_9char else budget.parent_9char
		parent = await cls.check_for_valid_parent(parent_9char, client_uuid)
		if budget_updates.name:
			await cls.check_for_existing_budget_by_name(budget_updates, budget.client_uuid)
		if budget_updates.parent_9char or budget_updates.budget_type:
			if budget_updates.parent_9char == budget_9char:
				return await ExceptionHandling.custom405("Cannot set same value for parent_9char and budget_9char.")
			else:
				child_budget = budget_updates if budget_updates.budget_type else budget
				if not await ClientSubBudgetActions.valid_child_budget(child_budget, parent):
					return await ExceptionHandling.custom405("Unable to set new parent budget.")
				else:
					budget.budget_type = budget_updates.budget_type
		if "value" in budget_updates.dict(exclude_unset=True):
			if budget.budget_type != 0 and await ClientSubBudgetActions.valid_child_budget(budget, parent):
				budget_updates.value, parent, passthroughList = await ClientSubBudgetActions.sub_budget_expenditure(budget, parent, budget_updates.value)
			else:
				budget_updates.value = await ClientSubBudgetActions.sub_budget_expenditure(budget, None, budget_updates.value)
		update_budget = budget_updates.dict(exclude_unset=True)
		for k,v in update_budget.items():
			setattr(budget, k, v)
		if budget.budget_type != 0 and ("value" in budget_updates.dict(exclude_unset=True)):
			budget = await BaseActions.update_without_lookup(budget)
			parent = await BaseActions.update_without_lookup(parent)
			if not passthroughList:
				return {"updated": budget}, {"static_parent": parent}
			else:
				passthroughList = await BaseActions.update_without_lookup(passthroughList)
				return {"updated": budget}, {"static_parent": parent}, {"passthrough_budgets_affected": passthroughList}			
		else:
			return await BaseActions.update_without_lookup(budget)

	@classmethod
	async def delete_budget(cls, budget_9char: str, client_uuid: str):
		budget = await cls.get_budget_by_9char_and_client_uuid(budget_9char, client_uuid)
		sub_budget = await ClientSubBudgetActions.get_all_sub_budgets(budget_9char, client_uuid)
		if sub_budget: #TODO: add check for `or program or program_event`
			return await ExceptionHandling.custom405(f"Unable to delete budget named: {budget.name}.")
		if budget.budget_type == 0 and budget.parent_9char is not None:
			parent = await cls.get_budget_by_9char_and_client_uuid(budget.parent_9char, client_uuid)
			parent.value += budget.value
			return [await BaseActions.delete_without_lookup(budget), await BaseActions.update_without_lookup(parent)]
		else:
			return await BaseActions.delete_without_lookup(budget)
