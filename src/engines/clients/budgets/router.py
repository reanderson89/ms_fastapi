from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/budgets")
async def get_budgets():
	return {"message": "Got all budgets"}

@router.get("/clients/{client_uuid}/budgets/{budget_7char}")
async def get_budget(budget_7char: str):
	return {"message": f"Got budgets for {budget_7char}"}

@router.post("/clients/{client_uuid}/budgets")
async def create_budget():
	return {"message": "Created budget"}

@router.put("/clients/{client_uuid}/budgets/{budget_7char}")
async def update_budget(budget_7char: str):
	return {"message": f"Updated budget for {budget_7char}"}

# this should only work if there are no programs associated with the budget
@router.delete("/clients/{client_uuid}/budgets/{budget_7char}")
async def delete_budget(budget_7char: str):
	return {"message": f"Deleted budget for {budget_7char}"}
