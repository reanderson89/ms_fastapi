from fastapi import APIRouter

router = APIRouter()

@router.get("/clients/{client_id}/programs/{program_id}/events")
async def get_events():
	return {"message": "Got all events"}

@router.get("/clients/{client_id}/programs/{program_id}/events/{event_id}")
async def get_event(event_id: str):
	return {"message": f"Got events for {event_id}"}

@router.post("/clients/{client_id}/programs/{program_id}/events")
async def create_event():
	return {"message": "Created event"}

@router.put("/clients/{client_id}/programs/{program_id}/events/{event_id}")
async def update_event(event_id: str):
	return {"message": f"Updated event for {event_id}"}

# not in endpoint specs
# @router.delete("/clients/{client_id}/programs/{program_id}/events/{event_id}")
# async def delete_event(event_id: str):
# 	return {"message": f"Deleted event for {event_id}"}
