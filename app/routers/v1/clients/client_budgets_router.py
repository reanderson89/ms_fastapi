from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Query, Depends
from app.database.config import engine
from app.actions.clients.budgets import BudgetActions as actions
from app.models.clients import ClientBudgetModel, ClientBudgetUpdate, ClientBudgetCreate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Budgets"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/budgets", response_model=List[ClientBudgetModel])
async def get_budgets(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=5, lte=25),
	session: Session = Depends(get_session)
):
	budgets = actions.get_all_budgets(ClientBudgetModel, client_uuid, offset, limit)
	# budgets = session.exec(
	# 	select(ClientBudgetModel)
	# 	.where(ClientBudgetModel.client_uuid == client_uuid)
	# 	.offset(offset)
	# 	.limit(limit)
	# 	).all()
	# ExceptionHandling.check404(budgets)
	return budgets

@router.get("/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def get_budget(
	client_uuid: str,
	budget_9char: str,
	session: Session = Depends(get_session)
):
	budget = actions.get_one_budget(ClientBudgetModel, budget_9char, client_uuid)
	# budget = session.exec(
	# 	select(ClientBudgetModel)
	# 	.where(ClientBudgetModel.budget_9char == budget_9char,
	# 			ClientBudgetModel.client_uuid == client_uuid)
	# ).one_or_none()
	# ExceptionHandling.check404(budget)
	return budget

@router.post("/budgets", response_model=(List[ClientBudgetModel] | ClientBudgetModel))
async def create_budget(
	client_uuid: str,
	new_budgets: (List[ClientBudgetCreate] | ClientBudgetCreate)
):
	budget = actions.create_budgets(ClientBudgetModel, new_budgets, client_uuid)
	return budget
	# return CommonRoutes.create_one_or_many(new_budgets)

@router.put("/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def update_budget(
		budget_9char: str,
		client_uuid: str,
		budget_updates: ClientBudgetUpdate,
		session: Session = Depends(get_session)
):
	budget = actions.update_budget(ClientBudgetModel, budget_9char, client_uuid, budget_updates)
	# budget = session.exec(
	# 	select(ClientBudgetModel)
	# 	.where(
	# 		ClientBudgetModel.budget_9char == budget_9char,
	# 		ClientBudgetModel.client_uuid == client_uuid
	# 	)
	# ).one_or_none()
	# ExceptionHandling.check404(budget)
	# update_budget = budget_updates.dict(exclude_unset=True)
	# for k,v in update_budget.items():
	# 	setattr(budget, k, v)
	# budget.time_updated = int(time())
	# session.add(budget)
	# session.commit()
	# session.refresh(budget)
	return budget

# this should only work if there are no programs associated with the budget
@router.delete("/budgets/{budget_9char}")
async def delete_budget(
	budget_9char: str,
	client_uuid: str,
	session: Session = Depends(get_session)
):
	budget = actions.delete_budget(ClientBudgetModel, budget_9char, client_uuid)
	return budget
	#TODO: add check for programs
	# budget = session.exec(
	# 	select(ClientBudgetModel)
	# 	.where(
	# 		ClientBudgetModel.budget_9char == budget_9char,
	# 		ClientBudgetModel.client_uuid == client_uuid
	# 	)
	# ).one_or_none()
	# ExceptionHandling.check404(budget)
	# session.delete(budget)
	# session.commit()
	# return {'ok': True, 'Deleted:': budget}
