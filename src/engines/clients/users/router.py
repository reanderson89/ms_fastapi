from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/users")
async def get_users():
	return {"message": "Got all users"}

@router.get("/clients/{client_id}/users/{user_id}")
async def get_user(user_id: int):
	return {"message": f"Got users for {user_id}"}

@router.post("/clients/{client_id}/users")
async def create_user():
	return {"message": "Created user"}

@router.put("/clients/{client_id}/users/{user_id}")
async def update_user(user_id: int):
	return {"message": f"Updated user for {user_id}"}

@router.delete("/clients/{client_id}/users/{user_id}")
async def delete_user(user_id: int):
	return {"message": f"Deleted user for {user_id}"}
