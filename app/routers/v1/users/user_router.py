import os
from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.actions.users import UserActions
from app.models.users import UserModel, UserUpdate

test_mode = os.getenv("TEST_MODE", False)

router = APIRouter(tags=["Users"])


@router.get("/users", response_model=list[UserModel])
async def get_users(
	query_params: dict = Depends(get_query_params)
):
	return await UserActions.get_all_users(query_params)


@router.get("/users/{user_uuid}", response_model_by_alias=True)
async def get_user(user_uuid: str, expand_services: bool = False):
	return await UserActions.get_user(user_uuid, expand_services)


@router.post("/users", response_model=UserModel)
async def create_user(users: dict):#(List[UserService] | UserService)):
	return await UserActions.create_user(users)


@router.put("/users/{user_uuid}", response_model=UserModel)
async def update_user(user_uuid: str, users_updates: UserUpdate):
	return await UserActions.update_user(user_uuid, users_updates)


@router.delete("/users/{user_uuid}")
async def delete_user(user_uuid: str):
	return await UserActions.delete_user(user_uuid)


def test_mode():
	from fastapi import HTTPException
	if not test_mode:
		raise HTTPException(status_code=404, detail="Not Found")


@router.delete("/delete_test_user/{user_uuid}")
async def delete_test_user(user_uuid: str, test_mode: None = Depends(test_mode)):
	from fastapi import Response
	await UserActions.delete_test_user(user_uuid)
	return Response(status_code=200, content="Test User Deleted")
