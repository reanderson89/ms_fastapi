from typing import List
from sqlmodel import Session, select
from fastapi import APIRouter, Query, Depends
from app.routers.v1.v1CommonRouting import CommonRoutes, ExceptionHandling
from app.database.config import engine
# from app.models.clients.budgets import ClientBudgetModel, ClientBudgetUpdate
from app.models.clients.budgets.budget_models import ClientBudgetModel, ClientBudgetUpdate

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Budgets"])

def get_session():
	with Session(engine) as session:
		yield session

@router.get("/budgets", response_model=List[ClientBudgetModel])
async def get_budgets(
	client_uuid: str,
	offset: int = 0,
	limit: int = Query(default=100, lte=100),
	session: Session = Depends(get_session)
):
	budgets = session.exec(
		select(ClientBudgetModel)
		.where(ClientBudgetModel.client_uuid == client_uuid)
		.offset(offset)
		.limit(limit)
		).all()
	ExceptionHandling.check404(budgets)
	return budgets

@router.get("/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def get_budget(budget_9char: str):
	return CommonRoutes.get_one(ClientBudgetModel, budget_9char)

@router.post("/budgets", response_model=ClientBudgetModel)
async def create_budget(budgets: (ClientBudgetModel | List[ClientBudgetModel])):
	return CommonRoutes.create_one_or_many(budgets)

@router.put("/budgets/{budget_9char}", response_model=ClientBudgetModel)
async def update_budget(budget_9char: str, budget_updates: ClientBudgetUpdate):
	return CommonRoutes.update_one(budget_9char, ClientBudgetModel, budget_updates)

# this should only work if there are no programs associated with the budget
@router.delete("/budgets/{budget_9char}")
async def delete_budget(budget_9char: str):
	#TODO: add check for programs
	return CommonRoutes.delete_one(budget_9char, ClientBudgetModel)
