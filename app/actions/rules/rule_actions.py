from app.exceptions import ExceptionHandling
from app.worker.temp_worker import TempWorker
from app.models.reward.reward_models import (
    ProgramRuleCreate,
    ProgramRuleUpdate,
    ProgramRuleRewardCountResponse,
    StagedRewardUpdate,
    RuleState
)
from burp.models.reward import ProgramRuleModelDB, StagedRewardModelDB, ProgramRuleModel
from burp.utils.base_crud import BaseCRUD
from app.actions.rewards.staged_reward_actions import StagedRewardActions
from app.worker.logging_format import init_logger

logger = init_logger()


class RuleActions:

    @classmethod
    async def handle_rule_state_change(cls, current_rule: ProgramRuleModelDB, updated_rule: ProgramRuleModelDB):
        initial_state = current_rule.state
        new_state = updated_rule.state

        if initial_state == RuleState.DRAFT.value and new_state == RuleState.ACTIVE.value:
            await cls.trigger_worker_reward_creation(updated_rule)
        elif initial_state == RuleState.ACTIVE.value:
            if new_state == RuleState.DRAFT.value:
                await StagedRewardActions.handle_delete_staged_rewards(updated_rule.company_id, updated_rule.uuid)
            elif new_state == RuleState.ACTIVE.value:
                recreate_rewards = await cls.handle_check_keys(current_rule, updated_rule)
                if recreate_rewards:
                    await StagedRewardActions.handle_delete_staged_rewards(updated_rule.company_id, updated_rule.uuid)
                    await cls.trigger_worker_reward_creation(updated_rule)
                else:
                    await cls.setup_staged_rewards_for_update(updated_rule)

    @staticmethod
    async def trigger_worker_reward_creation(rule: ProgramRuleModelDB):
        worker = TempWorker()
        worker.get_users_for_reward_creation(rule)

    @staticmethod
    async def handle_check_keys(current_rule: ProgramRuleModelDB, updated_rule: ProgramRuleModelDB):
        keys_to_check = {'rule_type', 'trigger_field', 'timing_type', 'anniversary_years', 'onboarding_period', 'days_prior'}
        return any(getattr(updated_rule, key, None) != getattr(current_rule, key, None) for key in keys_to_check)

    @staticmethod
    async def setup_staged_rewards_for_update(updated_rule: ProgramRuleModelDB):
        staged_rewards = await StagedRewardActions.get_staged_rewards_by_rule(updated_rule.company_id, updated_rule.uuid)
        staged_reward_update = StagedRewardUpdate(
            program_id=updated_rule.sending_managers_program_id,
            bucket_customization_id=updated_rule.bucket_customization_id,
            bucket_customization_price=updated_rule.bucket_customization_price
        )
        for reward in staged_rewards:
            await StagedRewardActions.update_staged_reward(reward.uuid, updated_rule.company_id, updated_rule.uuid, staged_reward_update)

    @staticmethod
    async def to_program_rule_db_model(rule_create: ProgramRuleCreate):
        return ProgramRuleModelDB(
            **rule_create.dict()
        )

    @classmethod
    async def create_rule(cls, rule_create: ProgramRuleCreate):
        rule = await cls.to_program_rule_db_model(rule_create)
        rule = await BaseCRUD.create(rule)
        if not rule:
            return await ExceptionHandling.custom400("Rule was not created.")
        if rule.state == RuleState.DRAFT.value:
            return rule
        await cls.trigger_worker_reward_creation(rule)
        return rule

    @staticmethod
    async def get_program_rules_by_company(company_id: int, filter_params: dict = None):
        return await BaseCRUD.get_all_where(
            ProgramRuleModelDB,
            [ProgramRuleModelDB.company_id == company_id],
            params=filter_params,
            pagination=False
        )

    @staticmethod
    async def get_distinct_company_ids():
        return await BaseCRUD.get_all_where(
            ProgramRuleModelDB,
            [],
            pagination=False,
            distinct_column=ProgramRuleModelDB.company_id
        )

    @staticmethod
    async def get_program_rule(company_id: int, rule_uuid: str):
        return await BaseCRUD.get_one_where(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ]
        )

    @staticmethod
    async def get_reward_count_for_rule(company_id: int, rule_uuid: str):
        count = await BaseCRUD.get_row_count(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.company_id == company_id
            ]
        )
        return ProgramRuleRewardCountResponse(
            staged_rewards=count,
            company_id=company_id,
            rule_uuid=rule_uuid
        )

    @classmethod
    async def update_program_rule(cls, company_id: int, rule_uuid: str, rule_update: ProgramRuleUpdate):
        current_rule = await RuleActions.get_program_rule(company_id, rule_uuid)
        updated_rule = await BaseCRUD.update(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ],
            rule_update
        )
        if not updated_rule:
            return await ExceptionHandling.custom400("Rule was not updated")
        await cls.handle_rule_state_change(current_rule, updated_rule)
        return updated_rule

    @staticmethod
    async def deactivate_program_rule(company_id: int, rule_uuid: str, state=RuleState.INACTIVE.value):
        deactivated_rule = await BaseCRUD.update(
            ProgramRuleModelDB,
            [
                ProgramRuleModelDB.company_id == company_id,
                ProgramRuleModelDB.uuid == rule_uuid
            ],
            ProgramRuleModel(state=state)
        )
        if not deactivated_rule:
            return await ExceptionHandling.custom404("No rule found for update")

        await StagedRewardActions.handle_delete_staged_rewards(company_id, rule_uuid)
        return deactivated_rule
