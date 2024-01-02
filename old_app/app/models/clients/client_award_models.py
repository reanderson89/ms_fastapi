from typing import Optional
from burp.utils.enums import AwardType, ChannelType
from burp.models.base_models import BasePydantic
from burp.utils.base_crud import BaseCRUD
from burp.models.award import AwardModelDB
from burp.models.client_award import ClientAwardModel


class ClientAwardCreate(BasePydantic):
    award_uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class ClientAwardUpdate(BasePydantic):
    award_uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]


class ClientAwardResponse(ClientAwardModel):
    channel: Optional[ChannelType]
    award_type: Optional[AwardType]
    value: Optional[int]

    def __init__(self, **data):
        super().__init__(**data)
        award = BaseCRUD.get_one(
            AwardModelDB,
            [AwardModelDB.uuid == self.award_uuid]
        )
        if award:
            self.channel = award.channel
            self.award_type = award.award_type
            self.value = award.value


class ClientAwardDelete(BasePydantic):
    ok: bool
    Deleted: ClientAwardModel
