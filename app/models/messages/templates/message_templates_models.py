from typing import List, Optional
from sqlmodel import Field, SQLModel

class MessageTemplateModel(SQLModel, table=False):
    __tablename__ = "message_template"

    uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
    channel: int = Field(default=None)
    body: str = Field(default=None)
    time_created: int
    time_update: int

class MessageTemplateUpdateModel(SQLModel, table=False):
    channel: Optional[int]
    body: Optional[str]
    time_updated: Optional[int]
