from sqlmodel import SQLModel, Field
from typing import Optional


class ClientUserModel(SQLModel, table=True):
    __tablename__ = 'client_user'

    uuid: str = Field(default=None, primary_key=True, index=True)
    user_uuid: str = Field(default=None, index=True, foreign_key="user.uuid")
    manager_uuid: str = Field(default=None, index=True, foreign_key="manager.uuid")
    department: str = Field(default=None, index=True)
    active: bool
    time_created: int
    time_updated: int


class ClientUserUpdate(SQLModel, table=False):
    manager_uuid: Optional[str] = None
    department: Optional[str] = None
    active: Optional[bool]
    time_updated: Optional[int]


