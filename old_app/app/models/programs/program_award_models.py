from typing import Optional
from burp.models.base_models import BasePydantic
from burp.models.client_award import ClientAwardModelDB
from app.models.clients.client_award_models import ClientAwardResponse
from burp.utils.base_crud import BaseCRUD
from burp.models.program_award import ProgramAwardModel


class ProgramAwardCreate(BasePydantic):
    name: str
    description: Optional[str]
    hero_image: Optional[str]


class ProgramAwardUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class ProgramAwardResponse(ProgramAwardModel):
    client_award_description: Optional[str]
    channel: Optional[int|str]
    award_type: Optional[int|str]
    value: Optional[int]

    def __init__(self, **data):
        super().__init__(**data)

        client_award = BaseCRUD.get_one(
            ClientAwardModelDB,
            [ClientAwardModelDB.client_award_9char == self.client_award_9char]
        )
        client_award = ClientAwardResponse(**client_award.to_dict())

        self.client_award_description = client_award.description
        self.channel = client_award.channel
        self.award_type = client_award.award_type
        self.value = client_award.value


class ProgramAwardDelete(BasePydantic):
    ok: bool
    Deleted: ProgramAwardModel
