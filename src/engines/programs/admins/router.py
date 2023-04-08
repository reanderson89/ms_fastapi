from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_uuid}/admins")
async def get_admins():
	return {"message": "Got all admins"}

@router.get("/clients/{client_uuid}/programs/{program_uuid}/admins/{admin_uuid}")
async def get_admin(admin_uuid: str):
	return {"message": f"Got admins for {admin_uuid}"}

@router.post("/clients/{client_uuid}/programs/{program_uuid}/admins")
async def create_admin():
	return {"message": "Created admin"}

@router.put("/clients/{client_uuid}/programs/{program_uuid}/admins/{admin_uuid}")
async def update_admin(admin_uuid: str):
	return {"message": f"Updated admin for {admin_uuid}"}

@router.delete("/clients/{client_uuid}/programs/{program_uuid}/admins/{admin_uuid}")
async def delete_admin(admin_uuid: str):
	return {"message": f"Deleted admin for {admin_uuid}"}
