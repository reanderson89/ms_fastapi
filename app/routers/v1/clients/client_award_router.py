from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.actions.clients.awards.client_award_actions import ClientAwardActions
from app.models.clients import ClientAwardModel, ClientAwardCreate, ClientAwardUpdate, ClientAwardResponse

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Awards"])


@router.get("/awards", response_model=list[ClientAwardModel])
async def get_awards(
	client_uuid: str,
	query_params: dict = Depends(get_query_params)

):
	return await ClientAwardActions.get_client_awards(client_uuid, query_params)


@router.get("/awards/{client_award_9char}", response_model=ClientAwardResponse)
async def get_award(
	client_uuid: str,
	client_award_9char: str
):
	return await ClientAwardActions.get_award(client_uuid, client_award_9char)
	# award = await ClientAwardActions.get_award(client_uuid, client_award_9char)
	# return await ClientAwardRead.init_class(award)



@router.post("/awards", response_model=list[ClientAwardModel] | ClientAwardModel)
async def create_award(
	client_uuid: str,
	awards: list[ClientAwardCreate] | ClientAwardCreate
):
	return await ClientAwardActions.create_award(client_uuid, awards)


@router.put("/awards/{client_award_9char}", response_model=ClientAwardModel)
async def update_award(
	client_uuid: str,
	client_award_9char: str,
	award_updates: ClientAwardUpdate
):
	return await ClientAwardActions.update_award(client_uuid, client_award_9char, award_updates)


# this should only work if there is no programs or segments associated with the award
@router.delete("/awards/{client_award_9char}")
async def delete_award(
	client_uuid: str,
	client_award_9char: str
):
	#TODO: add check for programs
	return await ClientAwardActions.delete_award(client_uuid, client_award_9char)
