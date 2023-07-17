from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params
from app.actions.awards import AwardActions
from app.models.award import AwardModelDB, AwardUpdate, AwardModel
from app.utilities.auth.auth_handler import Permissions
from app.models.uploads import UploadType

router = APIRouter(tags=["Awards"])


@router.get("/awards")
async def get_all_awards(
	client_uuid: Annotated[str, Depends(Permissions(level="2"))],
	query_params: dict = Depends(default_query_params),
) -> Page[AwardModel]:
	return await AwardActions.get_all_awards(query_params)


@router.get("/awards/{award_uuid}")
async def get_award(
		client_uuid: Annotated[str, Depends(Permissions(level="2"))],
		award_uuid: str
):
	return await AwardActions.get_award(award_uuid)


@router.get("/awards/{award_uuid}/upload")
async def get_award_upload_url(
		client_uuid: Annotated[str, Depends(Permissions(level="2"))],
		award_uuid: str,
		file_name: str,
		upload_type: UploadType
):
	return await AwardActions.get_upload_url(award_uuid, file_name, upload_type.value)


@router.post("/awards", response_model=(list[AwardModel] | AwardModel))
async def create_award(
	client_uuid: Annotated[str, Depends(Permissions(level="2"))],
	awards: (list[AwardModelDB] | AwardModelDB)
):
	return await AwardActions.create_award(awards)


@router.put("/awards/{award_uuid}", response_model=AwardModel)
async def update_award(
	client_uuid: Annotated[str, Depends(Permissions(level="2"))],
	award_uuid: str,
	award_updates: AwardUpdate
):
	return await AwardActions.update_award(
		award_uuid,
		award_updates
	)


# TODO: this should only work if there is no client_awards or program_awards associated with the award
@router.delete("/awards/{award_uuid}")
async def delete_award(
	client_uuid: Annotated[str, Depends(Permissions(level="2"))],
	award_uuid: str
):
	#TODO: add check for programs
	return await AwardActions.delete_award(award_uuid)
