from typing import Optional
from burp.models.base_models import BasePydantic
from burp.utils.base_crud import BaseCRUD
from burp.models.client_award import ClientAwardModelDB
from app.models.clients.client_award_models import ClientAwardResponse
from burp.models.segment_award import SegmentAwardModel


class SegmentAwardUpdate(BasePydantic):
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class SegmentAwardCreate(BasePydantic):
    client_award_9char: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class SegmentAwardResponse(SegmentAwardModel):
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

        self.channel = client_award.channel
        self.award_type = client_award.award_type
        self.value = client_award.value


class ProgramAwardDelete(BasePydantic):
    ok: bool
    Deleted: SegmentAwardModel
