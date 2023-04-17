from sqlmodel import SQLModel, Field


class ClientUserModel(SQLModel, table=True):
    __tablename__ = 'client_user'

    uuid: str = Field(default=None, primary_key=True, index=True)
    user_uuid: Field(default=None, index=True, foreign_key="user.uuid")
    manager_uuid: Field(default=None, index=True, foreign_key="manager.uuid")
    department: str = Field(default=None, index=True)
    active: bool
    time_created: int
    time_updated: int


class ClientUserUpdate(SQLModel, table=False):
    manager_uuid: str = Field(default=None)
    department: str = Field(default=None)
    active: bool
    time_updated: int


