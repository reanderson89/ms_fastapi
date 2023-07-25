from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class AwardModelDB(Base):
    __tablename__ = "award"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(default=None, index=True)
    description: Mapped[str] = mapped_column(default=None, index=False)
    hero_image: Mapped[str] = mapped_column(default=None, index=True)
    channel: Mapped[int] = mapped_column(default=None, index=True)
    award_type: Mapped[int] = mapped_column(default=None, index=True)
    value: Mapped[int] = mapped_column(default=None, index=True)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)

class AwardModel(BasePydantic):
    uuid: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    hero_image: Optional[str] = None
    channel: Optional[int] = None
    award_type: Optional[int] = None
    value: Optional[int] = None
    time_created: Optional[int] = None
    time_updated: Optional[int] = None

class AwardUpdate(BasePydantic):
    name: Optional[str] = None
    description: Optional[str] = None
    hero_image: Optional[str] = None
    channel: Optional[int] = None
    award_type: Optional[int] = None
    value: Optional[int] = None
