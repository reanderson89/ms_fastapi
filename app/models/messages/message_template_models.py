from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base_class import Base, BasePydantic

class MessageTemplateModel(Base):
    __tablename__ = "message_template"

    uuid: Mapped[str] = mapped_column(default=None, primary_key=True, index=True)
    channel: Mapped[int] = mapped_column(default=None)
    body: Mapped[str] = mapped_column(default=None)
    time_created: Mapped[int] = mapped_column(default=None)
    time_updated: Mapped[int] = mapped_column(default=None)

class MessageTemplateCreate(BasePydantic):
    channel: Optional[int]
    body: Optional[str]

class MessageTemplateUpdate(BasePydantic):
    channel: Optional[int]
    body: Optional[str]
