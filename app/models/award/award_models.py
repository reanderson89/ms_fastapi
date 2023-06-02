from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class AwardModel(Base):
	__tablename__ = "award"

	uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
	name: Mapped[str] = mapped_column(default=None, index=True)
	description: Mapped[str] = mapped_column(default=None, index=False)
	hero_image: Mapped[int] = mapped_column(default=None, index=True)
	channel: Mapped[int] = mapped_column(default=None, index=True)
	award_type: Mapped[int] = mapped_column(default=None, index=True)
	value: Mapped[int] = mapped_column(default=None, index=True)
	time_created: Mapped[int] = mapped_column(default=None)
	time_updated: Mapped[int] = mapped_column(default=None)


class AwardUpdate(BasePydantic):
	name: Optional[str] = None
	description: Optional[str] = None
	hero_image: Optional[int] = None
	channel: Optional[int] = None
	award_type: Optional[int] = None
	value: Optional[int] = None
