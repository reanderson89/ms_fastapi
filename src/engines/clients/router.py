from fastapi import APIRouter

router = APIRouter()

# not in endpoint specs
@router.get("/clients")
async def get_clients():
	return {"message": "Got all clients"}

@router.get("/clients/{client_uuid}")
async def get_client(client_uuid: str):
	return {"message": f"Got clients for {client_uuid}"}

@router.post("/clients")
async def create_client():
	return {"message": "Created client"}

@router.put("/clients/{client_uuid}")
async def update_client(client_uuid: str):
	return {"message": f"Updated client for {client_uuid}"}
