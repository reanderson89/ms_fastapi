from typing import Optional, Annotated
from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.actions.clients.budgets import ClientBudgetActions
from app.models.clients import ClientBudgetModelDB, ClientBudgetUpdate, ClientBudgetCreate, ClientBudgetModel
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Budgets"])

@router.get("/budgets")
async def get_budgets(
	client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
	client_uuid: str, 
	query_params=Depends(default_query_params)
) -> Page[ClientBudgetModel]:
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientBudgetActions.get_all_budgets(client_uuid, query_params)

@router.get("/budgets/{budget_9char}", response_model_by_alias=True)
async def get_budget(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		client_uuid: str,
		budget_9char: str,
		expanded: Optional[bool] = False):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientBudgetActions.get_one_budget(budget_9char, client_uuid, expanded)

@router.post("/budgets", response_model=ClientBudgetModelDB) #only allowed to create 1 at a time
async def create_budget(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		client_uuid: str,
		new_budget: ClientBudgetCreate):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientBudgetActions.create_budget(new_budget, client_uuid)

@router.put("/budgets/{budget_9char}")#, response_model=ClientBudgetModel)
async def update_budget(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		budget_9char: str,
		client_uuid: str,
		budget_updates: ClientBudgetUpdate):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientBudgetActions.update_budget(budget_updates, budget_9char, client_uuid)

# this should only work if there are no programs associated with the budget
@router.delete("/budgets/{budget_9char}")
async def delete_budget(
		client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
		budget_9char: str,
		client_uuid: str):
	await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
	return await ClientBudgetActions.delete_budget(budget_9char, client_uuid)
