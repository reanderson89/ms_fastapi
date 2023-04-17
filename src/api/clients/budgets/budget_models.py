from sqlmodel import Field, SQLModel


class ClientBudgetModel(SQLModel, table=True):
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
    name: str = Field(default=None)
    value: int = Field(default=0)
    time_updated: int
    active: int