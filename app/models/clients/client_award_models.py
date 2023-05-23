from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from typing import Optional

class ClientAwardModel(Base):
	__tablename__ = "client_award"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	client_uuid: Mapped[str] = mapped_column(default=None, index=True)
	award_9char: Mapped[str] = mapped_column(default=None, index=None)
	award_type: Mapped[int] = mapped_column(default=0)
	name: Mapped[str] = mapped_column(default=None)
	description: Mapped[str] = mapped_column(default=None)
	hero_image: Mapped[str] = mapped_column(default=None)
	channel: Mapped[int] = mapped_column(default=0)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)

class ClientAwardUpdate(BasePydantic):
	award_type: Optional[int] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[str] = None
	channel: Optional[int] = 0
	time_updated: Optional[int] = 0
