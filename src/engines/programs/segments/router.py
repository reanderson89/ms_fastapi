from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_uuid}/programs/{program_uuid}/segments")
async def get_segments():
	return {"message": "Got all segments"}

@router.get("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}")
async def get_segment(segment_uuid: str):
	return {"message": f"Got segments for {segment_uuid}"}

@router.post("/clients/{client_uuid}/programs/{program_uuid}/segments")
async def create_segment():
	return {"message": "Created segment"}

@router.put("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}")
async def update_segment(segment_uuid: str):
	return {"message": f"Updated segment for {segment_uuid}"}

@router.delete("/clients/{client_uuid}/programs/{program_uuid}/segments/{segment_uuid}")
async def delete_segment(segment_uuid: str):
	return {"message": f"Deleted segment for {segment_uuid}"}
