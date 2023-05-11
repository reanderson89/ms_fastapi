from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends
from app.actions.clients.budgets import ClientBudgetActions
from app.models.clients import ClientBudgetModel, ClientBudgetUpdate, ClientBudgetCreate
from app.actions.commonActions import CommonActions

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Budgets"])

@router.get("/budgets", response_model=List[ClientBudgetModel])
async def get_budgets(client_uuid: str, session: Session = Depends(CommonActions.get_session)):
	return await ClientBudgetActions.get_all_budgets(client_uuid, session)

@router.get("/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def get_budget(client_uuid: str, budget_9char: str, session: Session = Depends(CommonActions.get_session)):
	return await ClientBudgetActions.get_one_budget(budget_9char, client_uuid, session)

@router.post("/budgets", response_model=ClientBudgetModel) #only allowed to create 1 at a time
async def create_budget(client_uuid: str, new_budget: ClientBudgetCreate):
	return await ClientBudgetActions.create_budget(new_budget, client_uuid)

@router.put("/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def update_budget(budget_9char: str, client_uuid: str, budget_updates: ClientBudgetUpdate, session: Session = Depends(CommonActions.get_session)):
	return await ClientBudgetActions.update_budget(budget_updates, budget_9char, client_uuid, session)

# this should only work if there are no programs associated with the budget
@router.delete("/budgets/{budget_9char}")
async def delete_budget(budget_9char: str, client_uuid: str, session: Session = Depends(CommonActions.get_session)):
	return await ClientBudgetActions.delete_budget(budget_9char, client_uuid, session)
