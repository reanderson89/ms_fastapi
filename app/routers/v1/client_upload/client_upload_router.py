import os
from fastapi import APIRouter
from app.models.uploads import UploadFile, Uploadread, UploadType

from app.actions.clients.upload import ClientUploadActions


test_mode = os.getenv("TEST_MODE", False)

router = APIRouter(tags=["Upload"], prefix="/clients/{client_uuid}")


@router.get("/upload", response_model_by_alias=True)
async def get_upload_url(client_uuid: str, file_name: str, upload_type: UploadType):
	return await ClientUploadActions.get_upload_url(upload_type, file_name, client_uuid)


@router.post("/upload", response_model_by_alias=True)
async def post_upload_url(client_uuid: str, file_name:UploadFile):
	return await ClientUploadActions.process_roster_file(file_name, client_uuid)
