from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/awards")
async def get_awards():
	return {"message": "Got all awards"}

@router.get("/clients/{client_id}/awards/{award_id}")
async def get_award(award_id: int):
	return {"message": f"Got awards for {award_id}"}

@router.post("/clients/{client_id}/awards")
async def create_award():
	return {"message": "Created award"}

@router.put("/clients/{client_id}/awards/{award_id}")
async def update_award(award_id: int):
	return {"message": f"Updated award for {award_id}"}

@router.delete("/clients/{client_id}/awards/{award_id}")
async def delete_award(award_id: int):
	return {"message": f"Deleted award for {award_id}"}
