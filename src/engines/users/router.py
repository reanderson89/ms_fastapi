from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
	return {"message": "Got all users"}

@router.get("/users/{user_uuid}")
async def get_user(user_uuid: str):
	return {"message": f"Got users for {user_uuid}"}

@router.post("/users")
async def create_user():
	return {"message": "Created user"}

@router.put("/users/{user_uuid}")
async def update_user(user_uuid: str):
	return {"message": f"Updated user for {user_uuid}"}
