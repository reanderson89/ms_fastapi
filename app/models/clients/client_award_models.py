from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic
from typing import Optional

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

class ClientAwardUpdate(BasePydantic):
	award_uuid: Optional[str] = None
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[int] = None
	time_updated: Optional[int] = None
