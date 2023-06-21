from fastapi import APIRouter, Depends
from app.routers.v1.dependencies import get_query_params
from app.models.programs import ProgramRuleModel, ProgramRuleUpdate, ProgramRuleCreate
from app.actions.programs.rule.program_rule_actions import ProgramRuleActions

router = APIRouter(
	prefix="/clients/{client_uuid}/programs/{program_9char}",
	tags=["Client Program Rules"]
)


def path_params(client_uuid: str, program_9char: str, rule_9char: str=None):
	return {
		"client_uuid": client_uuid,
		"program_9char": program_9char,
		"rule_9char": rule_9char
	}


@router.get("/rules", response_model=list[ProgramRuleModel])
async def get_rules(
	path_params: dict = Depends(path_params),
	query_params: dict = Depends(get_query_params)
):
	return await ProgramRuleActions.get_all_rules(path_params, query_params)


@router.get("/rules/{rule_9char}", response_model=ProgramRuleModel)
async def get_rule(
	path_params: dict = Depends(path_params)
):
	return await ProgramRuleActions.get_rule(path_params)


@router.post("/rules", response_model=(list[ProgramRuleModel] | ProgramRuleModel))
async def create_rule(
	rules: (list[ProgramRuleCreate] | ProgramRuleCreate),
	path_params: dict = Depends(path_params),
	program_uuid: str = Depends(ProgramRuleActions.get_program_uuid)
):
	return await ProgramRuleActions.create_rule(rules, path_params, program_uuid)


@router.put("/rules/{rule_9char}", response_model=ProgramRuleModel)
async def update_rule(
	rule_updates: ProgramRuleUpdate,
	path_params: dict = Depends(path_params)
):
	return await ProgramRuleActions.update_rule(rule_updates, path_params)


@router.delete("/rules/{rule_9char}")
async def delete_rule(
	path_params: dict = Depends(path_params)
):
	return await ProgramRuleActions.delete_rule(path_params)
