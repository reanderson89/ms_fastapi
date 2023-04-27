from app.database.config import engine
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from typing import List
from time import time
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.utilities import SHA224Hash, timestampMilliseconds

class BudgetActions():

	def get_all_budgets(budget, client_uuid: str, offset: int, limit: int):
		with Session(engine) as session:
			budgets = session.exec(
				select(budget)
				.where(budget.client_uuid == client_uuid)
				.offset(offset)
				.limit(limit)
				).all()
			ExceptionHandling.check404(budgets)
			return budgets

	def get_one_budget(budget_model, budget_9char: str, client_uuid: str):
		with Session(engine) as session:
			budget = session.exec(
				select(budget_model)
				.where(budget_model.budget_9char == budget_9char,
						budget_model.client_uuid == client_uuid)
			).one_or_none()
			ExceptionHandling.check404(budget)
			return budget

	def create_budgets(budget_model, new_budgets, client_uuid: str):
		with Session(engine) as session:
			if isinstance(new_budgets, List):
				for budget in new_budgets:
					current_time = int(time())
					budget = budget_model(
						**budget.dict(),
						uuid=SHA224Hash(),
						client_uuid=client_uuid,
						time_created=current_time,
						time_updated=current_time
					)
					session.add(budget)
			else:
				current_time = int(time())
				new_budgets = budget_model(
					**new_budgets.dict(),
					uuid=SHA224Hash(),
					client_uuid=client_uuid,
					time_created=current_time,
					time_updated=current_time
				)
				session.add(new_budgets)

			session.commit()

			if isinstance(new_budgets, List):
				for budget in new_budgets:
					session.refresh(budget)
			else:
				session.refresh(new_budgets)
			return new_budgets

	def update_budget(budget_model, budget_updates, budget_9char: str, client_uuid: str):
		with Session(engine) as session:
			budget = session.exec(
				select(budget_model)
				.where(
					budget_model.budget_9char == budget_9char,
					budget_model.client_uuid == client_uuid
				)
			).one_or_none()
			ExceptionHandling.check404(budget)
			update_budget = budget_updates.dict(exclude_unset=True)
			for k,v in update_budget.items():
				setattr(budget, k, v)
			budget.time_updated = int(time())
			session.add(budget)
			session.commit()
			session.refresh(budget)
			return budget

	def delete_budget(budget_model, budget_9char: str, client_uuid: str):
		with Session(engine) as session:
			budget = session.exec(
				select(budget_model)
				.where(
					budget_model.budget_9char == budget_9char,
					budget_model.client_uuid == client_uuid
				)
			).one_or_none()
			ExceptionHandling.check404(budget)
			session.delete(budget)
			session.commit()
			return {'ok': True, 'Deleted:': budget}
