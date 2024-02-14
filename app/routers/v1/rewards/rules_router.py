from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path
from app.actions.rules.rule_actions import RuleActions
from app.models.reward.reward_models import (
    ProgramRuleCreate,
    ProgramRuleDelete,
    ProgramRuleResponse,
    ProgramRuleUpdate,
    ProgramRuleRewardCountResponse
)
from burp.utils.auth_utils import Permissions


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


@router.get("/program_rule/{company_id}/{rule_uuid}/reward_count", response_model=ProgramRuleRewardCountResponse)
async def get_reward_count_for_rule(
    company_id: int = Path(...),
    rule_uuid: str = Path(...)
):
    return await RuleActions.get_reward_count_for_rule(company_id, rule_uuid)


@router.post("/program_rule", response_model=ProgramRuleResponse)
async def create_program_rule(
    jwt: Annotated[str, Depends(Permissions(level="rails"))],
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
