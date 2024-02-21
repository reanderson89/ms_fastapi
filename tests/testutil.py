from collections import namedtuple
from burp.utils.utils import SHA224Hash


new_program_rule = {
    "company_id": 1,
    "segmented_by": [],
    "rule_name": "test program rule",
    "rule_type": "BIRTHDAY",
    "trigger_field": "birthday",
    "timing_type": "DAY_OF",
    "anniversary_years": [0],
    "onboarding_period": 0,
    "days_prior": 0,
    "sending_time": "9:00 AM",
    "timezone": "Pacific Time (US & Canada)",
    "manager_id": 3,
    "sending_managers_account_id": 12,
    "sending_managers_program_id": 68,
    "bucket_customization_id": 1234,
    "bucket_customization_price": 150,
    "subject": "test subject",
    "memo": "test memo",
    "recipient_note": "test note",
    "state": "ACTIVE",
    "company_values": ["these", "are", "values"],
    "created_by": 12,
    # "updated_by":
}

update_program_rule = {
    "rule_name": "updated test program rule",
    "rule_type": "BIRTHDAY",
    "trigger_field": "birthday",
    "timing_type": "DAY_OF",
    "anniversary_years": [0],
    "onboarding_period": 0,
    "days_prior": 0,
    "sending_time": "9:00 AM",
    "timezone": "Pacific Time (US & Canada)",
    "manager_id": 3,
    "sending_managers_account_id": 12,
    "sending_managers_program_id": 68,
    "bucket_customization_id": 1234,
    "bucket_customization_price": 150,
    "subject": "updated test subject",
    "memo": "updated test memo",
    "recipient_note": "updated test note",
    "company_values": ["these", "are", "updated", "values"],
    "segmented_by": [],
    "state": "ACTIVE",
    "updated_by": 12,
}

users_from_rails = {
    "company_id": 1,
    "users": [
        {
            "user_birthdate": 1234,
            "anniversary": 2,
            "employment_date": 2,
            "manager_id": 3,
            "department": "pytest",
            "city" : "city",
            "state" : "state",
            "country" : "country",
            "region": "region",
            "account_ID": 4
        },
        {
            "user_birthdate": 1234,
            "anniversary": 2,
            "employment_date": 2,
            "manager_id": 3,
            "department": "pytest",
            "city" : "city",
            "state" : "state",
            "country" : "country",
            "region": "region",
            "account_ID": 5
        }
    ]
}
