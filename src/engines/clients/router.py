from fastapi import APIRouter

router = APIRouter()

# not in endpoint specs
# @router.get("/clients")
# async def get_clients():
# 	return {"message": "Got all clients"}

@router.get("/clients/{client_id}")
async def get_client(client_id: int):
	return {"message": f"Got clients for {client_id}"}

@router.post("/clients")
async def create_client():
	return {"message": "Created client"}

@router.put("/clients/{client_id}")
async def update_client(client_id: int):
	return {"message": f"Updated client for {client_id}"}

# not in endpoint specs
# @router.delete("/clients/{client_id}")
# async def delete_client(client_id: int):
# 	return {"message": f"Deleted client for {client_id}"}
