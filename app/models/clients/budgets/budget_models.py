from typing import List, Optional
from sqlmodel import Field, SQLModel


class ClientBudgetModel(SQLModel, table=False):
    __tablename__ = "client_budget"

    uuid: str = Field(default=None, primary_key=True, index=True)
    client_uuid: str = Field(default=None, index=True, foreign_key="client.uuid")
    budget_9char: str = Field(default=None, index=True)
    parent_9char: str = Field(default=None, index=True)
    name: str = Field(default=None)
    value: int = Field(default=0)
    time_created: int
    time_updated: int
    active: int

class ClientBudgetUpdate(SQLModel, table=False):
    name: Optional[str] = Field(default=None)
    value: Optional[int] = Field(default=0)
    time_updated: Optional[int] = 0
    active: Optional[int] = 0
