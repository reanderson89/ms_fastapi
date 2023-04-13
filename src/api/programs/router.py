import fastapi as APIRouter

router = APIRouter.APIRouter()

@router.get("/clients/{client_uuid}/programs")
async def get_programs():
	return {"message": "Got all programs"}

@router.get("/clients/{client_uuid}/programs/{program_7char}")
async def get_program(program_7char: str):
	return {"message": f"Got programs for {program_7char}"}

@router.post("/clients/{client_uuid}/programs")
async def create_program():
	return {"message": "Created program"}

@router.put("/clients/{client_uuid}/programs/{program_7char}")
async def update_program(program_7char: str):
	return {"message": f"Updated program for {program_7char}"}

# should only work if there are no segments or events associated with the program
@router.delete("/clients/{client_uuid}/programs/{program_7char}")
async def delete_program(program_7char: str):
	return {"message": f"Deleted program for {program_7char}"}
