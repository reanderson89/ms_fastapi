from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/awards")
async def get_awards():
	return {"message": "Got all awards"}

@router.get("/clients/{client_uuid}/awards/{award_7char}")
async def get_award(award_7char: str):
	return {"message": f"Got awards for {award_7char}"}

@router.post("/clients/{client_uuid}/awards")
async def create_award():
	return {"message": "Created award"}

@router.put("/clients/{client_uuid}/awards/{award_7char}")
async def update_award(award_7char: str):
	return {"message": f"Updated award for {award_7char}"}

# this should only work if there is no programs or segments associated with the award
@router.delete("/clients/{client_uuid}/awards/{award_7char}")
async def delete_award(award_7char: str):
	return {"message": f"Deleted award for {award_7char}"}
