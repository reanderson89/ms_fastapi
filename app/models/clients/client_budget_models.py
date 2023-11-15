from typing import Optional
from pydantic import validator
from burp.utils.enums import BudgetType
from burp.models.base_models import BasePydantic
from burp.models.client import ClientModel
from burp.models.client_budget import ClientBudgetModel, ClientBudgetModelDB




class ClientBudgetCreate(BasePydantic):
    budget_9char: Optional[str]
    parent_9char: Optional[str]
    name: Optional[str]
    value: int
    active: Optional[bool] = True
    budget_type: Optional[BudgetType]

    @validator('budget_type', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientBudgetUpdate(BasePydantic):
    name: Optional[str]
    value: Optional[int] = 0
    parent_9char: Optional[str]
    time_updated: Optional[int] = 0
    active: Optional[bool]
    budget_type: Optional[BudgetType]

    @validator('budget_type', pre=False)
    def validate_award_type(cls, v, field):
        return field.type_[v].value


class ClientBudgetExpanded(ClientBudgetModel):
    client: Optional[ClientModel]
    subbudgets_expanded: Optional[list[ClientBudgetModel]]

class ClientBudgetShortExpand(ClientBudgetModel):
    client: Optional[ClientModel]
    subbudgets: Optional[ClientBudgetModel]


class BudgetResponse(ClientBudgetModel):
    pass


class BudgetDelete(BasePydantic):
    ok: bool = True
    Deleted: ClientBudgetModel


class DeleteResponse(BasePydantic):
    ok: bool = True
    Deleted: ClientBudgetModel
    Parent: Optional[ClientBudgetModel]

    @classmethod
    def format_data(cls, values):
        if isinstance(values, list):
            temp_dict = values[0]
            temp_dict['Parent'] = values[1]
            return temp_dict
        elif isinstance(values, ClientBudgetModelDB):
            values = {'Deleted': values}
        return values
