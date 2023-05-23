from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from pydantic import BaseModel
"""
Why is this here?

SQLAlchemy: Cannot use 'DeclarativeBase' 
directly as a declarative base class. 
Create a Base by creating a subclass of it.
"""

class Base(DeclarativeBase, MappedAsDataclass):#, dataclass_callable=pydantic.dataclasses.dataclass):
    pass

class BasePydantic(BaseModel):
    class Config:
        orm_mode = True