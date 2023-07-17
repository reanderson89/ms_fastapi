from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from app.models.base_class import Base, BasePydantic
from app.actions.base_actions import BaseActions
from app.actions.utils import new_9char
from app.models.clients.client_award_models import ClientAwardModelDB, ClientAwardResponse

class SegmentAward(Base):
	__tablename__ = "program_segment_award"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True)
	program_9char: Mapped[str] = mapped_column(default=None)
	program_award_9char: Mapped[str] = mapped_column(default=None)
	segment_9char: Mapped[str] = mapped_column(default=None)
	segment_award_9char: Mapped[str] = mapped_column(default=None)
	client_award_9char: Mapped[str] = mapped_column(default=None)
	client_uuid: Mapped[str] = mapped_column(default=None)
	name: Mapped[str] = mapped_column(default=None)
	description: Mapped[str] = mapped_column(default=None)
	hero_image: Mapped[str] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

	def __init__(self, **data):
		super().__init__(**data)
		if not self.segment_award_9char:
			self.segment_award_9char = new_9char()
		if not self.uuid:
			self.uuid = (self.client_uuid + self.program_9char + self.segment_9char + self.client_award_9char)

class SegmentAwardReturn(BasePydantic):
	uuid: str 
	client_uuid: str 
	program_9char: str 
	program_award_9char: str 
	segment_9char: str 
	segment_award_9char: str 
	client_award_9char: str
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None
	time_created: Optional[int] = None
	time_updated: Optional[int] = None

class SegmentAwardUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None

class SegmentAwardCreate(BasePydantic):
	client_award_9char: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None

class SegmentAwardBase(BasePydantic):
	uuid: Optional[str] = None 
	client_uuid: Optional[str] = None 
	program_9char: Optional[str] = None 
	program_award_9char: Optional[str] = None 
	segment_9char: Optional[str] = None 
	segment_award_9char: Optional[str] = None
	client_award_9char: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None
	time_created: Optional[int] = None
	time_updated: Optional[int] = None

class SegmentAwardResponse(SegmentAwardBase):
	channel: Optional[int] = None
	award_type: Optional[int] = None
	value: Optional[int] = None

	def __init__(self, **data):
		super().__init__(**data)

		client_award = BaseActions.get_one(
			ClientAwardModelDB,
			[ClientAwardModelDB.client_award_9char == self.client_award_9char]
		)
		client_award = ClientAwardResponse(**client_award.to_dict())

		self.channel = client_award.channel
		self.award_type = client_award.award_type
		self.value = client_award.value