from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules")
async def get_rules():
	return {"message": "Got all rules"}

@router.get("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
async def get_rule(rule_9char: str):
	return {"message": f"Got rules for {rule_9char}"}

@router.post("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules")
async def create_rule():
	return {"message": "Created rule"}

@router.put("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
async def update_rule(rule_9char: str):
	return {"message": f"Updated rule for {rule_9char}"}

@router.delete("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}/rules/{rule_9char}")
async def delete_rule(rule_9char: str):
	return {"message": f"Deleted rule for {rule_9char}"}
