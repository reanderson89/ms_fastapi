import fastapi as APIRouter

router = APIRouter.APIRouter()

@router.get("/clients/{client_id}/programs")
async def get_programs():
	return {"message": "Got all programs"}

@router.get("/clients/{client_id}/programs/{program_id}")
async def get_program(program_id: int):
	return {"message": f"Got programs for {program_id}"}

@router.post("/clients/{client_id}/programs")
async def create_program():
	return {"message": "Created program"}

@router.put("/clients/{client_id}/programs/{program_id}")
async def update_program(program_id: int):
	return {"message": f"Updated program for {program_id}"}

# should only work if there are no segments or events associated with the program
@router.delete("/clients/{client_id}/programs/{program_id}")
async def delete_program(program_id: int):
	return {"message": f"Deleted program for {program_id}"}
