from faker import Faker
from collections import namedtuple
from burp.utils.utils import SHA224Hash
import uuid

fake = Faker()

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
    "timezone": {
        "name": "Pacific Time (US & Canada)",
        "label": "Pacific Standard Time (GMT-8:00)",
        "value": "America/Los_Angeles"
    },
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


staged_rewards = [
    {
        "user_account_uuid": SHA224Hash(),
        "employee_id": fake.random_number(digits=5, fix_len=True),
        "company_id": 1,
        "state": "STAGED",  # or however you might want to mock this
        "rule_uuid": SHA224Hash(),
        "employee_account_id": fake.random_number(digits=5, fix_len=True),
        "gid": str(uuid.uuid4()),
        "program_id": fake.random_number(digits=5, fix_len=True),
        "bucket_customization_id": fake.random_number(digits=5, fix_len=True),
        "bucket_customization_price": fake.random_number(digits=5, fix_len=True),
        "first_name": "Bilbo",
        "last_name": "Baggins",
        "full_name": "Bilbo Baggins",  # To be filled after generating first and last names
        "email": "burglar@lotr.com",
        "send_on": "2025-04-12",
        "send_at": 9,
    },
    {
        "user_account_uuid": SHA224Hash(),
        "employee_id": fake.random_number(digits=5, fix_len=True),
        "company_id": 1,
        "state": "STAGED",  # or however you might want to mock this
        "rule_uuid": SHA224Hash(),
        "employee_account_id": fake.random_number(digits=5, fix_len=True),
        "gid": str(uuid.uuid4()),
        "program_id": fake.random_number(digits=5, fix_len=True),
        "bucket_customization_id": fake.random_number(digits=5, fix_len=True),
        "bucket_customization_price": fake.random_number(digits=5, fix_len=True),
        "first_name": "Gandalf",
        "last_name": "TheGrey",
        "full_name": "Gandalf TheGrey",  # To be filled after generating first and last names
        "email": "mythrandir@wizard.com",
        "send_on": "2025-04-13",
        "send_at": 9,
    },
    {
        "user_account_uuid": SHA224Hash(),
        "employee_id": fake.random_number(digits=5, fix_len=True),
        "company_id": 1,
        "state": "STAGED",  # or however you might want to mock this
        "rule_uuid": SHA224Hash(),
        "employee_account_id": fake.random_number(digits=5, fix_len=True),
        "gid": str(uuid.uuid4()),
        "program_id": fake.random_number(digits=5, fix_len=True),
        "bucket_customization_id": fake.random_number(digits=5, fix_len=True),
        "bucket_customization_price": fake.random_number(digits=5, fix_len=True),
        "first_name": "Samwise",
        "last_name": "Gamgee",
        "full_name": "Samwise Gamgee",  # To be filled after generating first and last names
        "email": "samthewise@hobbit.com",
        "send_on": "2025-04-13",
        "send_at": 9,
    }
]