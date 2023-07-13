from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params
from app.routers.v1.pagination import Page
from app.models.segments import SegmentModel, SegmentUpdate, SegmentCreate, SegmentReturn
from app.actions.segments import SegmentActions

router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}", tags=["Client Program Segments"])

def path_params(client_uuid: str, program_9char: str, segment_9char: str=None):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char,
		"segment_9char": segment_9char
	}

@router.get("/segments")
async def get_segments(
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(default_query_params)
) -> Page[SegmentReturn]:
	return await SegmentActions.get_all_segments(path_params, query_params)


@router.get("/segments/{segment_9char}", response_model=SegmentModel)
async def get_segment(
	path_params: dict = Depends(path_params),
):
	return await SegmentActions.get_segment(path_params)


@router.post("/segments", response_model=(list[SegmentModel] | SegmentModel))
async def create_segment(
	segments: (list[SegmentCreate] | SegmentCreate),
	path_params: dict = Depends(path_params),
):
	return await SegmentActions.create_segment(segments, path_params)


@router.put("/segments/{segment_9char}", response_model=SegmentModel)
async def update_segment(
	segment_updates: SegmentUpdate,
	path_params: dict = Depends(path_params)
):
	return await SegmentActions.update_segment(path_params, segment_updates)


@router.delete("/segments/{segment_9char}")
async def delete_segment(
	path_params: dict = Depends(path_params)
):
	return await SegmentActions.delete_segment(path_params)
