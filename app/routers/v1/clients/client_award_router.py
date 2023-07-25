from typing import Annotated

from fastapi import APIRouter, Depends
from app.routers.v1.pagination import Page
from app.routers.v1.dependencies import default_query_params, verify_client_award
from app.actions.clients.awards.client_award_actions import ClientAwardActions
from app.models.clients import ClientAwardModelDB, ClientAwardCreate, ClientAwardUpdate, ClientAwardResponse
from app.utilities.auth.auth_handler import Permissions, check_jwt_client_with_client
from app.models.uploads import UploadType

router = APIRouter(prefix="/clients/{client_uuid}", tags=["Client Awards"])


@router.get("/awards")
async def get_awards(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    query_params: dict = Depends(default_query_params)
) -> Page[ClientAwardResponse]:
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.get_client_awards(client_uuid, query_params)


@router.get("/awards/{client_award_9char}", response_model=ClientAwardResponse)
async def get_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    client_award_9char: str
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.get_award(client_uuid, client_award_9char)


@router.get(
        "/awards/{client_award_9char}/upload",
        dependencies=[Depends(verify_client_award)]
    )
async def get_award_upload_url(
    client_uuid: str,
    client_award_9char: str,
    file_name: str,
    upload_type: UploadType
):
    return await ClientAwardActions.get_upload_url(client_uuid, client_award_9char, file_name, upload_type.value)


@router.post("/awards", response_model=list[ClientAwardResponse] | ClientAwardResponse)
async def create_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    awards: list[ClientAwardCreate] | ClientAwardCreate
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.create_award(client_uuid, awards)


@router.put("/awards/{client_award_9char}", response_model=ClientAwardModelDB)
async def update_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    client_award_9char: str,
    award_updates: ClientAwardUpdate
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    return await ClientAwardActions.update_award(client_uuid, client_award_9char, award_updates)


# this should only work if there is no programs or segments associated with the award
@router.delete("/awards/{client_award_9char}")
async def delete_award(
    client_uuid_jwt: Annotated[str, Depends(Permissions(level="1"))],
    client_uuid: str,
    client_award_9char: str
):
    await check_jwt_client_with_client(client_uuid_jwt, client_uuid)
    #TODO: add check for programs
    return await ClientAwardActions.delete_award(client_uuid, client_award_9char)
