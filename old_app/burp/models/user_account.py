from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from burp.models.base_models import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class UserAccountModelDB(Base):
    __tablename__ = "user_account"

    uuid: Mapped[str] = mapped_column(String(65), default=None, primary_key=True, index=True)
    user_uuid: Mapped[str] = mapped_column(String(56), default=None, nullable=True)
    account_9char: Mapped[str] = mapped_column(String(9), default=None, nullable=True)
    account_id: Mapped[str] = mapped_column(Integer(11), default=None, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class UserAccountModel(BasePydantic):
    uuid: Optional[str]
    user_uuid: Optional[str]
    account_9char: Optional[str]
    account_id: Optional[int]
