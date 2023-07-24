from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import default_query_params, verify_segment_award
from app.routers.v1.pagination import Page
from app.actions.segments.awards import SegmentAwardActions
from app.models.uploads import UploadType
from app.models.segments.segment_award_models import SegmentAwardUpdate, SegmentAwardReturn, SegmentAwardCreate, SegmentAwardResponse


router = APIRouter(prefix="/clients/{client_uuid}/programs/{program_9char}/segments/{segment_9char}", tags=["Client Program Segment Awards"])


def path_params(
		client_uuid: str,
		program_9char: str,
		segment_9char: str,
		segment_award_9char: str=None,
		program_award_9char: str=None
	):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char,
		"segment_9char": segment_9char,
		"segment_award_9char": segment_award_9char,
		"program_award_9char": program_award_9char
	}

@router.get("/awards")
async def get_segment_awards(
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(default_query_params)
) -> Page[SegmentAwardReturn]:
	return await SegmentAwardActions.get_all_segment_awards(path_params, query_params)


@router.get("/awards/{segment_award_9char}", response_model=SegmentAwardResponse)
async def get_segment_award(
	path_params: dict = Depends(path_params)
):
	return await SegmentAwardActions.get_segment_award(path_params)


@router.get(
		"/awards/{segment_award_9char}/upload",
		dependencies=[Depends(verify_segment_award)]
	)
async def get_segment_award_upload_url(
	file_name: str,
	upload_type: UploadType,
	path_params: dict = Depends(path_params)
):
	return await SegmentAwardActions.get_segment_upload_url(path_params, file_name, upload_type.value)


@router.post("/awards/{program_award_9char}", response_model=(list[SegmentAwardResponse] | SegmentAwardResponse))
async def create_segment_award(
	segment_awards: list[SegmentAwardCreate] | SegmentAwardCreate,
	path_params: dict = Depends(path_params)
):
	return await SegmentAwardActions.create_segment_award(segment_awards, path_params)


@router.put("/awards/{segment_award_9char}", response_model=SegmentAwardResponse)
async def update_segment_award(
	segment_award_updates: SegmentAwardUpdate,
	path_params: dict = Depends(path_params)
):
	return await SegmentAwardActions.update_segment_award(path_params, segment_award_updates)


@router.delete("/awards/{segment_award_9char}")
async def delete_segment_award(
	path_params: dict = Depends(path_params)
):
	return await SegmentAwardActions.delete_segment_award(path_params)
