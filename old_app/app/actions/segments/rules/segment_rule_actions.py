from burp.utils.base_crud import BaseCRUD
from burp.utils.helper_actions import HelperActions
from burp.models.segment_rule import SegmentRuleModelDB
from burp.models.program import ProgramModelDB
from app.exceptions import ExceptionHandling

class SegmentRuleActions:

    @staticmethod
    async def get_program_uuid(program_9char: str):
        program =  await BaseCRUD.get_one_where(
            ProgramModelDB.uuid,
            [ProgramModelDB.program_9char == program_9char]
        )

        await ExceptionHandling.check404(program)

        return program

    @staticmethod
    async def get_all_segment_rules(path_params, query_params):
        return await BaseCRUD.get_all_where(
            SegmentRuleModelDB,
            [
                SegmentRuleModelDB.client_uuid == path_params["client_uuid"],
                SegmentRuleModelDB.program_9char == path_params["program_9char"],
                SegmentRuleModelDB.segment_9char == path_params["segment_9char"]
            ],
            query_params
        )

    @staticmethod
    async def get_segment_rule(path_params):
        return await BaseCRUD.get_one_where(
            SegmentRuleModelDB,
            [
                SegmentRuleModelDB.rule_9char == path_params["rule_9char"],
                SegmentRuleModelDB.client_uuid == path_params["client_uuid"],
                SegmentRuleModelDB.program_9char == path_params["program_9char"],
                SegmentRuleModelDB.segment_9char == path_params["segment_9char"]
            ]
        )

    @staticmethod
    async def create_rules(rules, path_params, program_uuid):
        if isinstance(rules, list):
            rules = [SegmentRuleModelDB(
                **rule.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_uuid = program_uuid,
                rule_9char = await HelperActions.generate_9char()
            ) for rule in rules]
            return await BaseCRUD.create(rules)
        rules = SegmentRuleModelDB(
            **rules.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_uuid = program_uuid,
                rule_9char = await HelperActions.generate_9char()
        )
        return await BaseCRUD.create(rules)

    @staticmethod
    async def update_rule(rule_updates, path_params):
        return await BaseCRUD.update(
            SegmentRuleModelDB,
            [
                SegmentRuleModelDB.rule_9char == path_params["rule_9char"],
                SegmentRuleModelDB.client_uuid == path_params["client_uuid"],
                SegmentRuleModelDB.program_9char == path_params["program_9char"],
                SegmentRuleModelDB.segment_9char == path_params["segment_9char"]
            ],
            rule_updates
        )

    @staticmethod
    async def delete_rule(path_params):
        return await BaseCRUD.delete_one(
            SegmentRuleModelDB,
            [
                SegmentRuleModelDB.rule_9char == path_params["rule_9char"],
                SegmentRuleModelDB.client_uuid == path_params["client_uuid"],
                SegmentRuleModelDB.program_9char == path_params["program_9char"],
                SegmentRuleModelDB.segment_9char == path_params["segment_9char"]
            ]
        )
