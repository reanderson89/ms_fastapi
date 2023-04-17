from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_9char}/segments")
async def get_segments():
	return {"message": "Got all segments"}

@router.get("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
async def get_segment(segment_9char: str):
	return {"message": f"Got segments for {segment_9char}"}

@router.post("/clients/{client_uuid}/programs/{program_9char}/segments")
async def create_segment():
	return {"message": "Created segment"}

@router.put("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
async def update_segment(segment_9char: str):
	return {"message": f"Updated segment for {segment_9char}"}

@router.delete("/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}")
async def delete_segment(segment_9char: str):
	return {"message": f"Deleted segment for {segment_9char}"}
