from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
	__tablename__ = "client"

	uuid = Column(String(56), primary_key=True, index=True)
	name = Column(String(255), index=True)
	description = Column(String(256), index=True)
	time_created = Column(Integer)
	time_updated = Column(Integer)
	time_ping = Column(Integer)
