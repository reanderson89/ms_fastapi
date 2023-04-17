from .budget_models import ClientBudgetModel, ClientBudgetUpdate
from src.database.config import engine
from api.clients.clients_models import ClientModel
from api import CommonRoutes, ExceptionHandling
from fastapi import APIRouter, Query, Depends
from typing import List
from sqlmodel import Session, select

router = APIRouter()

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/clients/{client_uuid}/budgets", response_model=List[ClientBudgetModel])
async def get_budgets(session: Session = Depends(get_session),
		    		offset: int = 0,
					limit: int = Query(default=100, lte=100)):
	budgets = session.exec(
		select(ClientBudgetModel)
		.join(ClientModel)
		.where(ClientBudgetModel.client_uuid == ClientModel.uuid)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(budgets)
	return budgets

@router.get("/clients/{client_uuid}/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def get_budget(budget_9char: str):
	return CommonRoutes.get_one(ClientBudgetModel, budget_9char)

@router.post("/clients/{client_uuid}/budgets", response_model=ClientBudgetModel)
async def create_budget(budgets: (ClientBudgetModel | List[ClientBudgetModel])):
	return CommonRoutes.create_one_or_many(budgets)

@router.put("/clients/{client_uuid}/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def update_budget(budget_9char: str, budget_updates: ClientBudgetUpdate):
	return CommonRoutes.update_one(budget_9char, ClientBudgetModel, budget_updates)

# this should only work if there are no programs associated with the budget
@router.delete("/clients/{client_uuid}/budgets/{budget_9char}")
async def delete_budget(budget_9char: str):
	#TODO: add check for programs
	return CommonRoutes.delete_one(budget_9char, ClientBudgetModel)
