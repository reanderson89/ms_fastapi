from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from app.actions.utils import new_9char
from app.models.clients.client_award_models import ClientAwardModelDB, ClientAwardResponse
from app.actions.base_actions import BaseActions

class ProgramAwardModelDB(Base):
	__tablename__ = "program_award"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	program_9char: Mapped[str] = mapped_column(default=None, index=None)
	program_award_9char: Mapped[str] = mapped_column(default=None, index=None)
	client_award_9char: Mapped[str] = mapped_column(default=None, index=None)
	name: Mapped[str] = mapped_column(default=None)
	description: Mapped[str] = mapped_column(default=None)
	hero_image: Mapped[str] = mapped_column(default=None)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

	def __init__(self, **data):
		super().__init__(**data)
		if not self.program_award_9char:
			self.program_award_9char = new_9char()
		if not self.uuid:
			self.uuid = (self.client_uuid + self.program_9char + self.client_award_9char)


class ProgramAwardCreate(BasePydantic):
	name: str
	description: Optional[str] = None
	hero_image: Optional[str] = None


class ProgramAwardUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None


class ProgramAwardBase(BasePydantic):
	uuid: Optional[str] = None
	client_uuid: Optional[str] = None
	program_9char: Optional[str] = None
	program_award_9char: Optional[str] = None
	client_award_9char: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None
	time_created: Optional[int] = None
	time_updated: Optional[int] = None


class ProgramAwardResponse(ProgramAwardBase):
	client_award_description: Optional[str]
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

		self.client_award_description = client_award.description
		self.channel = client_award.channel
		self.award_type = client_award.award_type
		self.value = client_award.value
