from app.models.reward.reward_models import RuleType, TimingType
from app.actions.rewards.staged_reward_actions import StagedRewardActions


def test_birthday_day_of(test_dates):
    send_times = StagedRewardActions.calculate_send_dates(
        test_dates.birthate,
        RuleType.BIRTHDAY,
        TimingType.DAY_OF,
        current_date=test_dates.today
    )
    assert send_times == ["2024-12-22"]


def test_birthday_days_prior(test_dates):
    send_times = StagedRewardActions.calculate_send_dates(
        test_dates.birthate,
        RuleType.BIRTHDAY,
        TimingType.DAYS_PRIOR,
        days_prior=5,
        current_date=test_dates.today
    )
    assert send_times == ["2024-12-17"]


def test_birthday_weekday_week(test_dates):
    send_times = StagedRewardActions.calculate_send_dates(
        test_dates.birthate,
        RuleType.BIRTHDAY,
        TimingType.WEEKDAY_WEEK,
        current_date=test_dates.today
    )
    assert send_times == ["2024-12-16"]


def test_birthday_weekday_month(test_dates):
    send_times = StagedRewardActions.calculate_send_dates(
        test_dates.birthate,
        RuleType.BIRTHDAY,
        TimingType.WEEKDAY_MONTH,
        current_date=test_dates.today
    )
    assert send_times == ["2024-12-02"]


def test_onboarding_day_of(test_dates):
    send_times = StagedRewardActions.calculate_send_dates(
        test_dates.hired_on,
        RuleType.ONBOARDING,
        TimingType.DAY_OF,
        onboarding_period=91,
        current_date=test_dates.today
    )
    assert send_times == ["2024-05-14"]


def test_anniversary_day_of(test_dates):
    send_times = StagedRewardActions.calculate_send_dates(
        test_dates.anniversary,
        RuleType.ANNIVERSARY,
        TimingType.DAY_OF,
        anniversary_years=[1, 2, 3],
        current_date=test_dates.today
    )
    assert send_times == ["2025-01-13", "2026-01-13", "2027-01-13"]


def test_anniversary_days_prior(test_dates):
    send_dates = StagedRewardActions.calculate_send_dates(
        test_dates.anniversary,
        RuleType.ANNIVERSARY,
        TimingType.DAYS_PRIOR,
        days_prior=5,
        anniversary_years=[1, 2, 3],
        current_date=test_dates.today
    )
    assert send_dates == ["2025-01-08", "2026-01-08", "2027-01-08"]


def test_anniversary_weekday_week(test_dates):
    send_dates = StagedRewardActions.calculate_send_dates(
        test_dates.anniversary,
        RuleType.ANNIVERSARY,
        TimingType.WEEKDAY_WEEK,
        anniversary_years=[1, 2, 3],
        current_date=test_dates.today
    )
    assert send_dates == ["2025-01-13", "2026-01-12", "2027-01-11"]


def test_anniversary_weekday_month(test_dates):
    send_dates = StagedRewardActions.calculate_send_dates(
        test_dates.anniversary,
        RuleType.ANNIVERSARY,
        TimingType.WEEKDAY_MONTH,
        anniversary_years=[1, 2, 3],
        current_date=test_dates.today
    )
    assert send_dates == ["2025-01-01", "2026-01-01", "2027-01-01"]
