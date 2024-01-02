from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from burp.utils.enums import BudgetType
from burp.models.base_models import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class ClientBudgetModelDB(Base):
    __tablename__ = "client_budget"

    uuid: Mapped[str] = mapped_column(String(65), default=None, primary_key=True, index=True)
    client_uuid: Mapped[str] = mapped_column(String(56), default=None, index=True, nullable=True)
    budget_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    parent_9char: Mapped[str] = mapped_column(String(9), default=None, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), default=None, nullable=True)
    value: Mapped[int] = mapped_column(Integer(11), default=0, nullable=True)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=True)
    budget_type: Mapped[int] = mapped_column(Integer(11), default=0, nullable=True)


class ClientBudgetModel(BasePydantic):
    uuid: Optional[str]
    client_uuid: Optional[str]
    budget_9char: Optional[str]
    parent_9char: Optional[str]
    name: Optional[str]
    value: Optional[int]
    time_created: Optional[int]
    time_updated: Optional[int]
    active: Optional[bool]
    budget_type: Optional[BudgetType]
