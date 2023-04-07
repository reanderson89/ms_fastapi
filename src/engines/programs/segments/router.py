from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/programs/{program_id}/segments")
async def get_segments():
	return {"message": "Got all segments"}

@router.get("/clients/{client_id}/programs/{program_id}/segments/{segment_id}")
async def get_segment(segment_id: int):
	return {"message": f"Got segments for {segment_id}"}

@router.post("/clients/{client_id}/programs/{program_id}/segments")
async def create_segment():
	return {"message": "Created segment"}

@router.put("/clients/{client_id}/programs/{program_id}/segments/{segment_id}")
async def update_segment(segment_id: int):
	return {"message": f"Updated segment for {segment_id}"}

@router.delete("/clients/{client_id}/programs/{program_id}/segments/{segment_id}")
async def delete_segment(segment_id: int):
	return {"message": f"Deleted segment for {segment_id}"}
