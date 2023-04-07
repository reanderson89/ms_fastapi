from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/programs/{program_id}/segments/{segment_id}/rules")
async def get_rules():
	return {"message": "Got all rules"}

@router.get("/clients/{client_id}/programs/{program_id}/segments/{segment_id}/rules/{rule_id}")
async def get_rule(rule_id: int):
	return {"message": f"Got rules for {rule_id}"}

@router.post("/clients/{client_id}/programs/{program_id}/segments/{segment_id}/rules")
async def create_rule():
	return {"message": "Created rule"}

@router.put("/clients/{client_id}/programs/{program_id}/segments/{segment_id}/rules/{rule_id}")
async def update_rule(rule_id: int):
	return {"message": f"Updated rule for {rule_id}"}

@router.delete("/clients/{client_id}/programs/{program_id}/segments/{segment_id}/rules/{rule_id}")
async def delete_rule(rule_id: int):
	return {"message": f"Deleted rule for {rule_id}"}
