from fastapi import APIRouter

router = APIRouter()

# not in specs
@router.get("/clients/{client_uuid}/users")
async def get_users():
	return {"message": "Got all users"}

# not in specs
@router.get("/clients/{client_uuid}/users/{user_uuid}")
async def get_user(user_uuid: str):
	return {"message": f"Got users for {user_uuid}"}

@router.post("/clients/{client_uuid}/users")
async def create_user():
	return {"message": "Created user"}

@router.put("/clients/{client_uuid}/users/{user_uuid}")
async def update_user(user_uuid: str):
	return {"message": f"Updated user for {user_uuid}"}

#
@router.delete("/clients/{client_uuid}/users/{user_uuid}")
async def delete_user(user_uuid: str):
	return {"message": f"Deleted user for {user_uuid}"}
