from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_7char}/segments")
async def get_segments():
	return {"message": "Got all segments"}

@router.get("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}")
async def get_segment(segment_7char: str):
	return {"message": f"Got segments for {segment_7char}"}

@router.post("/clients/{client_uuid}/programs/{program_7char}/segments")
async def create_segment():
	return {"message": "Created segment"}

@router.put("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}")
async def update_segment(segment_7char: str):
	return {"message": f"Updated segment for {segment_7char}"}

@router.delete("/clients/{client_uuid}/programs/{program_7char}/segments/{segment_7char}")
async def delete_segment(segment_7char: str):
	return {"message": f"Deleted segment for {segment_7char}"}
