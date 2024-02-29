from fastapi import APIRouter, Body, Path
from app.actions.rules.rule_actions import RuleActions
from app.models.reward.reward_models import (
    ProgramRuleCreate,
    ProgramRuleResponse,
    ProgramRuleUpdate
)


router = APIRouter(tags=["Program Rule"])


@router.get("/program_rule/{company_id}", response_model=list[ProgramRuleResponse])
async def get_program_rules_by_company(
    company_id: int = Path(...)
):
    return await RuleActions.get_program_rules_by_company(company_id)


@router.get("/program_rule/{company_id}/{rule_uuid}", response_model=ProgramRuleResponse|None)
async def get_program_rule(
    company_id: int = Path(...),
    rule_uuid: str = Path(...)
):
    return await RuleActions.get_program_rule(company_id, rule_uuid)


@router.post("/program_rule", response_model=ProgramRuleResponse)
async def create_program_rule(
    rule_create: ProgramRuleCreate = Body(...)
):
    return await RuleActions.create_rule(rule_create)


@router.put("/program_rule/{company_id}/{rule_uuid}", response_model=ProgramRuleResponse|None)
async def update_program_rule(
    company_id: int = Path(...),
    rule_uuid: str = Path(...),
    rule_update: ProgramRuleUpdate = Body(...)
):
    return await RuleActions.update_program_rule(company_id, rule_uuid, rule_update)


@router.delete("/program_rule/{company_id}/{rule_uuid}", response_model=ProgramRuleResponse)
async def delete_program_rule(
    company_id: int = Path(...),
    rule_uuid: str = Path(...)
):
    return await RuleActions.deactivate_program_rule(company_id, rule_uuid)
