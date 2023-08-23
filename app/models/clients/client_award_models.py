from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.actions.utils import new_9char
from app.enums import AwardType, ChannelType
from app.models.base_class import Base, BasePydantic
from app.actions.base_actions import BaseActions
from app.models.award.award_models import AwardModelDB

class ClientAwardModelDB(Base):
    __tablename__ = "client_award"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(default=None, index=True)
    client_award_9char: Mapped[str] = mapped_column(default=None, index=None)
    award_uuid: Mapped[str] = mapped_column(default=0)
    name: Mapped[str] = mapped_column(default=None)
    description: Mapped[str] = mapped_column(default=None)
    hero_image: Mapped[str] = mapped_column(default=None)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        if not self.client_award_9char:
            self.client_award_9char = new_9char()
        if not self.uuid:
            self.uuid = self.client_uuid + self.client_award_9char


class ClientAwardModel(BasePydantic):
    uuid: str
    client_uuid: Optional[str]
    client_award_9char: Optional[str]
    award_uuid: Optional[str]
    name: Optional[str]
    description: Optional[str]
    hero_image: Optional[str]
    time_created: Optional[int]
    time_updated: Optional[int]


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
        award = BaseActions.get_one(
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
