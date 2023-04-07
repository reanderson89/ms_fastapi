from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
	return {"message": "Got all users"}

@router.get("/users/{user_id}")
async def get_user(user_id: int):
	return {"message": f"Got users for {user_id}"}

@router.post("/users")
async def create_user():
	return {"message": "Created user"}

@router.put("/users/{user_id}")
async def update_user(user_id: int):
	return {"message": f"Updated user for {user_id}"}
