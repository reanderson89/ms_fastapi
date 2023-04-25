from sqlmodel import SQLModel, Field
from typing import Optional

class ClientUserModel(SQLModel, table=True):
    __tablename__ = 'client_user'

    uuid: str = Field(default=None, primary_key=True, index=True, max_length=56)
    user_uuid: str = Field(default=None, index=True, foreign_key="user.uuid", max_length=56)
    client_uuid: str = Field(default=None, index=True, foreign_key="client.uuid", max_length=56)
    manager_uuid: str = Field(default=None, index=True, foreign_key="user.uuid", max_length=56)
    title: str = Field(default=None, max_length=255)
    department: str = Field(default=None, index=True, max_length=255)
    active: bool
    time_created: int = None
    time_updated: int = None
    time_hire: int = None
    time_start: int = None
    admin: int

class ClientUserUpdate(SQLModel, table=False):
    manager_uuid: Optional[str] = Field(default=None, max_length=56)
    department: Optional[str] = Field(default=None, max_length=255)
    active: Optional[bool] = Field(default=None)
    time_updated: Optional[int]
    admin: Optional[int] = Field(default=None)
