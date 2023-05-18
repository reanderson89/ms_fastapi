from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends
from app.actions.clients.budgets import ClientSubBudgetActions, ClientBudgetActions
from app.models.clients import ClientBudgetModel, ClientBudgetUpdate, ClientBudgetCreate
from app.actions.commonActions import CommonActions

router = APIRouter(prefix="/clients/{client_uuid}/budgets/{parent_9char}/sub", tags=["Client Sub-Budgets"])

@router.get("/", response_model=List[ClientBudgetModel])
async def get_sub_budgets(client_uuid: str, parent_9char: str, session: Session = Depends(CommonActions.get_session)):
	return await ClientSubBudgetActions.get_all_sub_budgets(client_uuid, parent_9char, session)

@router.get("/{budget_9char}", response_model=ClientBudgetModel)
async def get_sub_budget(client_uuid: str, budget_9char: str, session: Session = Depends(CommonActions.get_session)):
	return await ClientBudgetActions.get_one_budget(budget_9char, client_uuid, session)

@router.post("/", response_model=ClientBudgetModel) #only allowed to create 1 at a time
async def create_sub_budget(client_uuid: str, new_budget: ClientBudgetCreate):
	return await ClientSubBudgetActions.create_sub_budget(new_budget, client_uuid)

@router.put("/{budget_9char}", response_model=ClientBudgetModel)
async def update_sub_budget(budget_9char: str, client_uuid: str, budget_updates: ClientBudgetUpdate, session: Session = Depends(CommonActions.get_session)):
	return await ClientSubBudgetActions.update_sub_budget(budget_updates, budget_9char, client_uuid, session)

# this should only work if there are no programs associated with the budget
@router.delete("/{budget_9char}")
async def delete_sub_budget(budget_9char: str, client_uuid: str, session: Session = Depends(CommonActions.get_session)):
	return await ClientSubBudgetActions.delete_sub_budget(budget_9char, client_uuid, session)
