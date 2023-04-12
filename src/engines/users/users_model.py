from sqlmodel import Field, SQLModel

class UsersModel(SQLModel, table=True):
	__tablename__ = "user"

	uuid: str = Field(default=None, primary_key=True, index=True)
	first_name: str = Field(default=None, index=True)
	last_name: str = Field(default=None, index=True)
	latitude: int
	longitude: int
	time_created: int
	time_updated: int
	time_ping: int

class UsersUpdate(SQLModel, table=False):
	first_name: str = None
	last_name: str = None
	latitude: int = None
	longitude: int = None
	time_updated: int = None
	time_ping: int = None