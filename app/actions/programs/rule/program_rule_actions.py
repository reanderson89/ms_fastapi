from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.programs.program_models import ProgramModelDB
from app.models.programs.program_rule_models import ProgramRuleModelDB


class ProgramRuleActions:

    @staticmethod
    async def get_program_uuid(program_9char: str):
        return await BaseActions.get_one_where(
			ProgramModelDB.uuid,
			[ProgramModelDB.program_9char == program_9char]
		)
    
    @staticmethod
    async def get_rule(path_params):
        return await BaseActions.get_one_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.rule_9char == path_params["rule_9char"],
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ]
        )
    
    @staticmethod
    async def get_all_rules(path_params, query_params):
        return await BaseActions.get_all_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ],
            query_params
            )

    @staticmethod
    async def create_rule(rules, path_params, program_uuid):
        if isinstance(rules, list):
            rules = [ProgramRuleModelDB(
                **rule.dict(),
                program_uuid = program_uuid,
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                rule_9char = await HelperActions.generate_9char()
            ) for rule in rules]
        else:
            rules = ProgramRuleModelDB(
                **rules.dict(),
                program_uuid = program_uuid,
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                rule_9char = await HelperActions.generate_9char() 
            )
        return await BaseActions.create(rules)
    
    @staticmethod
    async def update_rule(rule_updates, path_params):
        return await BaseActions.update(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.rule_9char == path_params["rule_9char"],
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"]
            ],
            rule_updates
        )
    
    @staticmethod
    async def delete_rule(path_params):
        return await BaseActions.delete_one(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.rule_9char == path_params["rule_9char"],
                ProgramRuleModelDB.program_9char == path_params["program_9char"],
                ProgramRuleModelDB.client_uuid == path_params["client_uuid"] 
            ]
        )


