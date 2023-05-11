from typing import Optional, List
from sqlmodel import Field, SQLModel


class ClientBudgetModel(SQLModel, table=True):
    __tablename__ = "client_budget"

    uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
    client_uuid: str = Field(default=None, index=True, max_length=56)
    budget_9char: str = Field(default=None, index=True, max_length=9)
    parent_9char: str = Field(default=None, index=True, max_length=9)
    name: str = Field(default=None, max_length=255)
    value: int = Field(default=0)
    time_created: int = None
    time_updated: int = None
    active: bool = Field(default=True)

class ClientBudgetCreate(SQLModel, table=False):
    budget_9char: Optional[str] = None
    parent_9char: Optional[str] = None
    name: Optional[str] = None
    value: int = None
    active: Optional[bool]

class ClientBudgetUpdate(SQLModel, table=False):
    name: Optional[str] = Field(default=None, max_length=255)
    value: Optional[int] = 0
    parent_9char: Optional[str] = None
    time_updated: Optional[int] = 0
    active: Optional[bool]

# class ClientBudgetExpanded(ClientBudgetModel):
#     client: Optional[List[ClientModel]]
#     #subbudgets: Optional[List[SubBudgetModel]]
    
