import fastapi as APIRouter

router = APIRouter.APIRouter()

@router.get("/clients/{client_uuid}/programs")
async def get_programs():
	return {"message": "Got all programs"}

@router.get("/clients/{client_uuid}/programs/{program_uuid}")
async def get_program(program_uuid: int):
	return {"message": f"Got programs for {program_uuid}"}

@router.post("/clients/{client_uuid}/programs")
async def create_program():
	return {"message": "Created program"}

@router.put("/clients/{client_uuid}/programs/{program_uuid}")
async def update_program(program_uuid: int):
	return {"message": f"Updated program for {program_uuid}"}

# should only work if there are no segments or events associated with the program
@router.delete("/clients/{client_uuid}/programs/{program_uuid}")
async def delete_program(program_uuid: int):
	return {"message": f"Deleted program for {program_uuid}"}
