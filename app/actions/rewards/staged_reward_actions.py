import calendar
from datetime import datetime, timedelta  # , timezone
from zoneinfo import ZoneInfo
from app.models.reward.reward_models import (
    RewardState,
    RuleType,
    StagedRewardUpdate,
    RewardState,
    StagedRewardCountResponse,
    TimingType
)
from app.worker.logging_format import init_logger
from burp.models.reward import ProgramRuleModel, StagedRewardModelDB
from burp.utils.base_crud import BaseCRUD

logger = init_logger()


class StagedRewardActions:

    @staticmethod
    async def to_staged_reward_db_model(user: dict, rule: ProgramRuleModel, send_on: str, send_at: str):
        return StagedRewardModelDB(
            user_account_uuid=user["user_account_uuid"],
            employee_id=user["employee_id"],
            company_id=rule.company_id,
            state=RewardState.STAGED.value,
            rule_uuid=rule.uuid,
            employee_account_id=user["account_id"],
            gid=user["account_gid"],
            program_id=rule.sending_managers_program_id,
            bucket_customization_id=rule.bucket_customization_id,
            bucket_customization_price=rule.bucket_customization_price,
            first_name=user["first_name"],
            last_name=user["last_name"],
            full_name=f"{user['first_name']} {user['last_name']}",
            email=user["email"],
            send_on=send_on,
            send_at=send_at
        )

    @staticmethod 
    async def get_staged_rewards_by_rule(company_id: int, rule_uuid: str):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.company_id == company_id,
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ],
            pagination=False
        )
    
    @classmethod
    async def get_reward_count_for_rule(cls, company_id: int):
        from app.actions.rules.rule_actions import RuleActions
        company_rules = await RuleActions.get_program_rules_by_company(company_id)
        response = {}
        for rule in company_rules:
            response[rule.uuid] = await BaseCRUD.get_row_count(
                StagedRewardModelDB,
                [
                    StagedRewardModelDB.rule_uuid == rule.uuid,
                    StagedRewardModelDB.company_id == company_id,
                    StagedRewardModelDB.state == RewardState.STAGED.value
                ]
            )
        return StagedRewardCountResponse(
            rules=response
        )
    
    @staticmethod
    async def get_staged_rewards(company_id: int, query_params: dict):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.company_id == company_id
            ],
            query_params
        )

    @staticmethod
    async def handle_delete_staged_rewards(company_id: int, rule_uuid: str):
        return await BaseCRUD.delete_all(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.company_id == company_id,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ]
        )

    @staticmethod
    async def update_staged_reward(staged_reward_uuid: str, company_id: int, rule_uuid: str, staged_reward_update: StagedRewardUpdate):
        return await BaseCRUD.update(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.uuid == staged_reward_uuid,
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.company_id == company_id
            ],
            staged_reward_update
        )

    @classmethod
    async def create_staged_reward(cls, users: list, rule: ProgramRuleModel):
        rewards_to_create = []
        for user in users:
            send_dates = await cls.get_send_times(user, rule)
            for send_on in send_dates:
                utc_send_on, utc_send_at = await cls.adjust_send_info_utc(send_on, rule.sending_time, rule.timezone)
                # send_at = await cls.convert_time_to_24_hour(rule.sending_time)
                db_reward = await cls.to_staged_reward_db_model(user, rule, utc_send_on, utc_send_at)
                rewards_to_create.append(db_reward)
        return await BaseCRUD.create(rewards_to_create)

    @staticmethod
    async def get_staged_rewards_by_date_and_time(send_on: str, send_at: int):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.send_on == send_on,
                StagedRewardModelDB.send_at == send_at,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ],
            pagination=False
        )
    
    @staticmethod
    async def get_staged_reward(staged_reward_uuid: str):
        return await BaseCRUD.get_one_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.uuid == staged_reward_uuid
            ]
        )

    @staticmethod
    async def get_staged_rewards_by_rule(company_id: int, rule_uuid: str):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.company_id == company_id,
                StagedRewardModelDB.rule_uuid == rule_uuid,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ],
            pagination=False
        )

    @staticmethod
    async def convert_time_to_24_hour(sending_time):
        # Split the time string into its components
        time_part, am_pm = sending_time.split(' ')
        hour = int(time_part.split(':')[0])

        # Adjust hour based on am/pm
        if am_pm.lower() == 'am' and hour == 12:
            # Midnight edge case
            send_at = 0
        elif am_pm.lower() == 'pm' and hour != 12:
            # Afternoon times excluding 12 PM
            send_at = hour + 12
        else:
            # Morning times and 12 PM
            send_at = hour

        return send_at

    @classmethod
    async def adjust_send_info_utc(cls, sending_date, sending_time, timezone):
        sending_datetime_str = f"{sending_date} {sending_time}"
        sending_datetime = datetime.strptime(sending_datetime_str, "%Y-%m-%d %I:%M %p")
        
        sending_timezone = ZoneInfo(timezone)
        local_datetime = sending_datetime.replace(tzinfo=sending_timezone)
        
        utc_datetime = local_datetime.astimezone(ZoneInfo("UTC"))
        
        utc_date = utc_datetime.strftime("%Y-%m-%d")
        utc_hour = utc_datetime.hour
            
        return utc_date, utc_hour

    @classmethod
    async def get_send_times(cls, user: dict, program_rule: ProgramRuleModel):
        rule_type = RuleType(program_rule.rule_type)
        timing_type = TimingType(program_rule.timing_type)

        # Parse epoch times to datetime
        birthday = datetime.fromtimestamp(user["time_birthday"])
        hired_on_date = datetime.fromtimestamp(user["hired_on"])
        onboard_date = hired_on_date
        # onboard_date = hired_on_date + timedelta(days=90)

        # today = datetime.now(timezone(timedelta(hours=-8))).date()
        today = datetime.now()
        match rule_type:
            case RuleType.BIRTHDAY:
                trigger_value = birthday
            case RuleType.ANNIVERSARY:
                trigger_value = hired_on_date
            case RuleType.ONBOARDING:
                trigger_value = onboard_date

        next_anniversary = cls.calculate_send_dates(
            trigger_date=trigger_value,
            rule_type=rule_type,
            timing_type=timing_type,
            timezone=program_rule.timezone,
            days_prior=program_rule.days_prior,
            anniversary_years=program_rule.anniversary_years,
            onboarding_period=program_rule.onboarding_period,
            current_date=today
        )
        return next_anniversary

    @classmethod
    def calculate_send_dates(
        cls,
        trigger_date: datetime,
        rule_type: RuleType,
        timing_type: TimingType,
        timezone: str | None = None,
        days_prior: int | None = None,
        anniversary_years: list | None = None,
        onboarding_period: int | None = None,
        current_date: datetime | None = None
    ):
        """
        Calculate the next send date based on the specified rule_type and timing_type.

        :param trigger_date: The date that triggers the send date.
        :param rule_type: The type of rule (Enum RuleType).
        :param timing_type: The type of timing adjustment to apply (Enum TimingType).
        :param days_prior: Number of days to adjust if DAYS_PRIOR is selected.
        :param anniversary_years: List of years to calculate anniversaries for.
        :param onboarding_period: Number of days after the trigger_date for onboarding rules.
        :param current_date: The current date to use for calculations.
        :return: A list of send dates in the format "YYYY-MM-DD".
        """
        # Initialize default values
        timezone = timezone or "UTC"
        days_prior = days_prior or 0
        anniversary_years = anniversary_years or []
        onboarding_period = onboarding_period or 0
        current_date = current_date or datetime.now()
        send_dates = []

        # Adjust dates based on rule_type
        if rule_type == RuleType.BIRTHDAY:
            send_date = cls.adjust_for_leap_year(
                datetime(year=current_date.year, month=trigger_date.month, day=trigger_date.day),
                current_date
            )
            if current_date > send_date:
                send_date = send_date.replace(year=current_date.year + 1)
            send_dates.append(send_date)
        elif rule_type == RuleType.ONBOARDING:
            send_date = trigger_date + timedelta(days=onboarding_period)
            send_dates.append(send_date)
        elif rule_type == RuleType.ANNIVERSARY:
            send_dates.extend(cls.calculate_anniversary_dates(trigger_date, current_date, anniversary_years))
        else:
            logger.error(f"Invalid rule_type: {rule_type}")
            raise ValueError(f"Invalid rule_type: {rule_type}")

        # Adjust dates based on timing_type
        send_dates = [cls.adjust_date_based_on_timing_type(date, timing_type, days_prior) for date in send_dates]
        return [date.strftime("%Y-%m-%d") for date in send_dates]

    @staticmethod
    async def get_staged_rewards_by_date_and_time(send_on: str, send_at: int):
        return await BaseCRUD.get_all_where(
            StagedRewardModelDB,
            [
                StagedRewardModelDB.send_on == send_on,
                StagedRewardModelDB.send_at == send_at,
                StagedRewardModelDB.state == RewardState.STAGED.value
            ],
            pagination=False
        )
    
    def adjust_for_leap_year(date: datetime, current_date: datetime):
        """
        Adjust the date for leap years if necessary.

        :param date: The date to adjust.
        :param current_date: The current date to use for calculations.
        :return: The adjusted date.
        """
        if date.month == 2 and date.day == 29 and not calendar.isleap(current_date.year):
            return datetime(year=current_date.year, month=3, day=1)
        return date

    @staticmethod
    def calculate_anniversary_dates(
        trigger_date: datetime,
        current_date: datetime,
        anniversary_years: list[int]
    ):
        """
        Calculate the next send date for each year in anniversary_years.

        :param trigger_date: The date that triggers the send date.
        :param current_date: The current date to use for calculations.
        :param anniversary_years: List of years to calculate anniversaries for.
        :return: A list of send dates.
        """
        send_dates = []
        for year in anniversary_years:
            anniversary_date = trigger_date.replace(year=trigger_date.year + year)
            if anniversary_date < current_date:
                anniversary_date = anniversary_date.replace(year=current_date.year + year + 1)
            send_dates.append(anniversary_date)
        return send_dates

    @staticmethod
    def adjust_date_based_on_timing_type(
        send_date: datetime,
        timing_type: TimingType,
        days_prior: int | None = None
    ):
        """
        Adjusts the send_date based on the specified timing_type and additional parameters.

        :param send_date: The original date to be adjusted.
        :param timing_type: The type of timing adjustment to apply (Enum TimingType).
        :param days_prior: Number of days to adjust if DAYS_PRIOR is selected.
        :return: The adjusted send_date.
        """
        days_prior = days_prior or 0
        if timing_type == TimingType.DAY_OF:
            pass  # send_date is already set
        elif timing_type == TimingType.DAYS_PRIOR:
            # Subtract days_prior from the send_date
            send_date -= timedelta(days=days_prior)
        elif timing_type == TimingType.WEEKDAY_WEEK:
            # Find the first weekday(i.e. MOnday) of the week
            send_date -= timedelta(days=send_date.weekday())
        elif timing_type == TimingType.WEEKDAY_MONTH:
            # Find the first weekday of the month
            first_of_month = send_date.replace(day=1)
            send_date = first_of_month + timedelta(days=(7 - first_of_month.weekday()) % 7 if first_of_month.weekday() > 4 else 0)
        return send_date
