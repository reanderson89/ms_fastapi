from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/programs/{program_id}/admins")
async def get_admins():
	return {"message": "Got all admins"}

@router.get("/clients/{client_id}/programs/{program_id}/admins/{admin_id}")
async def get_admin(admin_id: int):
	return {"message": f"Got admins for {admin_id}"}

@router.post("/clients/{client_id}/programs/{program_id}/admins")
async def create_admin():
	return {"message": "Created admin"}

@router.put("/clients/{client_id}/programs/{program_id}/admins/{admin_id}")
async def update_admin(admin_id: int):
	return {"message": f"Updated admin for {admin_id}"}

@router.delete("/clients/{client_id}/programs/{program_id}/admins/{admin_id}")
async def delete_admin(admin_id: int):
	return {"message": f"Deleted admin for {admin_id}"}
