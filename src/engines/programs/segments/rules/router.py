from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules")
async def get_rules():
	return {"message": "Got all rules"}

@router.get("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
async def get_rule(rule_uuid: str):
	return {"message": f"Got rules for {rule_uuid}"}

@router.post("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules")
async def create_rule():
	return {"message": "Created rule"}

@router.put("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
async def update_rule(rule_uuid: str):
	return {"message": f"Updated rule for {rule_uuid}"}

@router.delete("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/rules/{rule_uuid}")
async def delete_rule(rule_uuid: str):
	return {"message": f"Deleted rule for {rule_uuid}"}
