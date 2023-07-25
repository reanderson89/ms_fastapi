from enum import Enum
from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


"""
Why is this here?

SQLAlchemy: Cannot use 'DeclarativeBase'
directly as a declarative base class.
Create a Base by creating a subclass of it.
"""

class Base(DeclarativeBase, MappedAsDataclass):#, dataclass_callable=pydantic.dataclasses.dataclass):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class BasePydantic(BaseModel):
    class Config:
        orm_mode = True


class BaseEnum(Enum):
    def __getitem__(self, item):
        return self.__class__.__members__[item]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, cls):
            return v.name

        if isinstance(v, int):
            return cls(v).name

        if isinstance(v, str) and v in cls.__members__:
            return cls[v].name

        raise ValueError("Invalid value")
