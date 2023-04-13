from pydantic import BaseModel

class ClientBase(BaseModel):
	uuid: str
	name: str
	description: str
	time_created: int
	time_updated: int
	time_ping: int

class ClientCreate(ClientBase):
	pass

class Client(ClientBase):
	class Config:
		orm_mode = True

class ClientUpdate(BaseModel):
	name: str = None
	description: str = None
	time_updated: int = None
	time_ping: int = None
