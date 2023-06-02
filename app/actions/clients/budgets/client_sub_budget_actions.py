from sqlalchemy import select
from sqlalchemy.orm import Session
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.models.clients import ClientBudgetModel, budget_types
from app.actions.helper_actions import HelperActions

class ClientSubBudgetActions:

	@staticmethod
	async def get_sub_budget_type(budget):
		return budget_types[budget.budget_type]

	@classmethod
	async def create_sub_budget(cls, new_budget, parent, session: Session):
		try:
			budget_class = await cls.get_sub_budget_type(new_budget)
			budget, parent = await budget_class.create_budget(new_budget, parent)
			budget = ClientBudgetModel(
				**new_budget.dict(),
				uuid = await HelperActions.generate_UUID(),
				client_uuid = parent.client_uuid
			)
			budget.budget_9char = await HelperActions.generate_9char()
		except Exception as e:
			return await ExceptionHandling.custom405(f"Unable to complete creation of budget: {new_budget.name}.\nReason: {e.detail}")
		else: #if no exception is generated, then commit changes to db
			budget = await CommonRoutes.create_one_or_many(budget)
			session.add(parent)
			session.commit()
			session.refresh(parent)
			return budget


	@staticmethod
	async def get_all_sub_budgets(budget_9char, client_uuid, session):
		return session.scalars(
			select(ClientBudgetModel)
			.where(ClientBudgetModel.client_uuid == client_uuid,
					ClientBudgetModel.parent_9char == budget_9char)
		).all()


	@classmethod
	async def sub_budget_expenditure(cls, budget, parent, expenditure, session):
		budget_class = await cls.get_sub_budget_type(budget)
		if budget.budget_type != 0:
			static_parent, passthroughCap = await cls.find_next_static_budget(budget, session)
			for item in passthroughCap:
				item.value += expenditure
				if item.value + expenditure > 0:
					return await ExceptionHandling.custom405(f"Not enough passthrough budget in {item.name}")
			budget, static_parent = await budget_class.budget_expenditure(budget, static_parent, expenditure)
			return budget.value, static_parent, passthroughCap
		else:
			budget = await budget_class.budget_expenditure(budget, expenditure)
			return budget

	@staticmethod
	async def valid_child_budget(budget, parent):
		return budget.budget_type in budget_types[parent.budget_type].valid_child_type

	@staticmethod
	async def find_next_static_budget(budget, session):
		budgetExpendList = []
		while budget.budget_type != 0:
			budget = session.scalars(
				select(ClientBudgetModel)
				.where(ClientBudgetModel.budget_9char == budget.parent_9char,
						ClientBudgetModel.client_uuid == budget.client_uuid)
			).one_or_none()
			if budget.budget_type == 2:
				budgetExpendList.append(budget)
		return budget, budgetExpendList
