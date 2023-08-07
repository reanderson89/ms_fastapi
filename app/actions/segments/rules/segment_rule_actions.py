from app.actions.base_actions import BaseActions
from app.actions.helper_actions import HelperActions
from app.models.segments.segment_rule_models import SegmentRuleModel
from app.models.programs.program_models import ProgramModelDB

class SegmentRuleActions:

    @staticmethod
    async def get_program_uuid(program_9char: str, check404: bool = True):
        return await BaseActions.get_one_where(
            ProgramModelDB.uuid,
            [ProgramModelDB.program_9char == program_9char],
            check404
        )

    @staticmethod
    async def get_all_segment_rules(path_params, query_params):
        return await BaseActions.get_all_where(
            SegmentRuleModel,
            [
                SegmentRuleModel.client_uuid == path_params["client_uuid"],
                SegmentRuleModel.program_9char == path_params["program_9char"],
                SegmentRuleModel.segment_9char == path_params["segment_9char"]
            ],
            query_params
        )
    
    @staticmethod
    async def get_segment_rule(path_params):
        return await BaseActions.get_one_where(
            SegmentRuleModel,
            [
                SegmentRuleModel.rule_9char == path_params["rule_9char"],
                SegmentRuleModel.client_uuid == path_params["client_uuid"],
                SegmentRuleModel.program_9char == path_params["program_9char"],
                SegmentRuleModel.segment_9char == path_params["segment_9char"]
            ]
        )
    
    @staticmethod
    async def create_rules(rules, path_params, program_uuid):
        if isinstance(rules, list):
            rules = [SegmentRuleModel(
                **rule.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_uuid = program_uuid,
                rule_9char = await HelperActions.generate_9char()
            ) for rule in rules]
            return await BaseActions.create(rules)
        rules = SegmentRuleModel(
            **rules.dict(),
                client_uuid = path_params["client_uuid"],
                program_9char = path_params["program_9char"],
                segment_9char = path_params["segment_9char"],
                program_uuid = program_uuid,
                rule_9char = await HelperActions.generate_9char()
        )
        return await BaseActions.create(rules)
    
    @staticmethod
    async def update_rule(rule_updates, path_params):
        return await BaseActions.update(
            SegmentRuleModel,
            [
                SegmentRuleModel.rule_9char == path_params["rule_9char"],
                SegmentRuleModel.client_uuid == path_params["client_uuid"],
                SegmentRuleModel.program_9char == path_params["program_9char"],
                SegmentRuleModel.segment_9char == path_params["segment_9char"]
            ],
            rule_updates
        )

    @staticmethod
    async def delete_rule(path_params):
        return await BaseActions.delete_one(
            SegmentRuleModel,
            [
                SegmentRuleModel.rule_9char == path_params["rule_9char"],
                SegmentRuleModel.client_uuid == path_params["client_uuid"],
                SegmentRuleModel.program_9char == path_params["program_9char"],
                SegmentRuleModel.segment_9char == path_params["segment_9char"]
            ]
        )