from typing import List, Optional
from sqlmodel import Field, SQLModel
from time import time
# from pydantic import UUID4


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
    active: int

class ClientBudgetCreate(SQLModel, table=False):
    budget_9char: str = None
    parent_9char: str = None
    name: str = None
    value: int = None
    active: int

    # def __init__(self, **data):
    #     super().__init__(**data)
    #     current_time = int(time())
    #     self.time_created = current_time
    #     self.time_updated = current_time

class ClientBudgetUpdate(SQLModel, table=False):
    name: Optional[str] = Field(default=None, max_length=255)
    value: Optional[int] = 0
    time_updated: Optional[int] = 0
    active: Optional[int] = 0
