from typing import Optional
from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from burp.models.base_models import Base, BasePydantic
from sqlalchemy.dialects import mysql
Integer = mysql.INTEGER


class RewardModelDB(Base):
    __tablename__ = "reward"

    uuid: Mapped[str] = mapped_column(String(56), default=None, primary_key=True, index=True)
    client_admin_id: Mapped[str] = mapped_column(Integer(), default=None, index=True, nullable=False)
    company_id: Mapped[str] = mapped_column(Integer(), default=None, index=True, nullable=False)
    rule: Mapped[str] = mapped_column("rule", JSON, default=None, index=False, nullable=False)
    users: Mapped[str] = mapped_column("users", JSON, default=None, index=False, nullable=False)
    reward_info: Mapped[str] = mapped_column("reward_info", JSON, default=None, index=False, nullable=False)
    time_created: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)
    time_updated: Mapped[int] = mapped_column(Integer(11), default=None, nullable=True)


class RewardModel(BasePydantic):
    uuid: str
    client_admin_id: int
    company_id: int
    rule: dict
    users: Optional[list[dict]]
    reward_info: dict
