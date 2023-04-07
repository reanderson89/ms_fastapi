from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/budgets")
async def get_budgets():
	return {"message": "Got all budgets"}

@router.get("/clients/{client_id}/budgets/{budget_id}")
async def get_budget(budget_id: int):
	return {"message": f"Got budgets for {budget_id}"}

@router.post("/clients/{client_id}/budgets")
async def create_budget():
	return {"message": "Created budget"}

@router.put("/clients/{client_id}/budgets/{budget_id}")
async def update_budget(budget_id: int):
	return {"message": f"Updated budget for {budget_id}"}

@router.delete("/clients/{client_id}/budgets/{budget_id}")
async def delete_budget(budget_id: int):
	return {"message": f"Deleted budget for {budget_id}"}
