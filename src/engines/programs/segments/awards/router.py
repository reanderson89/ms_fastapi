from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards")
async def get_awards():
	return {"message": "Got all awards"}

@router.get("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
async def get_award(award_uuid: str):
	return {"message": f"Got awards for {award_uuid}"}

@router.post("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards")
async def create_award():
	return {"message": "Created award"}

@router.put("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
async def update_award(award_uuid: str):
	return {"message": f"Updated award for {award_uuid}"}

@router.delete("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}/awards/{award_uuid}")
async def delete_award(award_uuid: str):
	return {"message": f"Deleted award for {award_uuid}"}
