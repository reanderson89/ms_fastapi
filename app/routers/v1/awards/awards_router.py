from typing import List
from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.actions.awards import AwardActions
from app.models.award import AwardModel, AwardUpdate

router = APIRouter(tags=["Awards"])


@router.get("/awards", response_model=List[AwardModel])
async def get_all_awards(
	query_params: dict = Depends(get_query_params),
):
	return await AwardActions.get_all_awards(query_params)


@router.get("/awards/{award_uuid}", response_model=AwardModel)
async def get_award(
	award_uuid: str
):
	return await AwardActions.get_award(award_uuid)


@router.post("/awards", response_model=(List[AwardModel] | AwardModel))
async def create_award(
	awards: (List[AwardModel] | AwardModel)
):
	return await AwardActions.create_award(awards)


@router.put("/awards/{award_uuid}", response_model=AwardModel)
async def update_award(
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
	award_uuid: str
):
	#TODO: add check for programs
	return await AwardActions.delete_award(award_uuid)
