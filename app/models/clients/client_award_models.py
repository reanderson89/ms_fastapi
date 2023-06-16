from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from app.actions.utils import new_9char
from app.actions.base_actions import BaseActions
from app.models.award.award_models import AwardModel

class ClientAwardModel(Base):
	__tablename__ = "client_award"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	client_award_9char: Mapped[str] = mapped_column(default=None, index=None)
	award_uuid: Mapped[str] = mapped_column(default=0)
	name: Mapped[str] = mapped_column(default=None)
	description: Mapped[str] = mapped_column(default=None)
	hero_image: Mapped[int] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

	def __init__(self, **data):
		super().__init__(**data)
		if not self.client_award_9char:
			self.client_award_9char = new_9char()
		if not self.uuid:
			self.uuid = self.client_uuid + self.client_award_9char


class ClientAwardCreate(BasePydantic):
	award_uuid: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[int] = None


class ClientAwardUpdate(BasePydantic):
	award_uuid: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[int] = None


class ClientAwardBase(BasePydantic):
	uuid: str
	client_uuid: Optional[str] = None
	client_award_9char: Optional[str] = None
	award_uuid: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[int] = None
	time_created: Optional[int] = None
	time_updated: Optional[int] = None


class ClientAwardResponse(ClientAwardBase):
	channel: Optional[int] = None
	award_type: Optional[int] = None
	value: Optional[int] = None

	def __init__(self, **data):
		super().__init__(**data)
		award = BaseActions.get_one(
			AwardModel,
			[AwardModel.uuid == self.award_uuid]
		)
		if award:
			self.channel = award.channel
			self.award_type = award.award_type
			self.value = award.value
