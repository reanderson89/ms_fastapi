from sqlmodel import Field, SQLModel
from typing import List, Optional

class ClientAwardModel(SQLModel, table=False):
    __tablename__ = "client_award"

    uuid: str = Field(default=None, primary_key=True, index=True)
    client_uuid: str = Field(default=None, index=True, foreign_key="client.uuid")
    award_9char: str = Field(default=None, index=None)
    award_type: int = Field(default=0)
    name: str = Field(default=None)
    description: str = Field(default=None)
    hero_image: str = Field(default=None)
    channel: int = Field(default=0)
    time_created: int
    time_updated: int

class ClientAwardUpdate(SQLModel, table=False):
    award_type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    hero_image: Optional[str] = None
    channel: Optional[int] = 0
    time_updated: Optional[int] = 0
