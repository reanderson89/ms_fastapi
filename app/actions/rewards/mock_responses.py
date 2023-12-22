from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from faker import Faker

fake = Faker()


### Mock GET accounts response ###

now = datetime.now(timezone(timedelta(hours=-8)))

today = now.isoformat()
ninety_days_ago = (now - timedelta(days=90)).isoformat()
one_year_ago = (now - relativedelta(years=1)).isoformat()
three_years_ago = (now - relativedelta(years=3)).isoformat()
twenty_years_ago = (now - relativedelta(years=20)).isoformat()
thirty_five_years_ago = (now - relativedelta(years=35)).isoformat()
just_a_date = datetime(2000, 1, 1, 0, 0).isoformat()

mock_user_accounts = {
    "accounts": [
        {
            "id": 38098,
            "gid": "fbb9f443-cf24-42b1-bf3d-ac14172de5ae",
            "first_name": "Tiger",
            "last_name": "Woods",
            "deactivated_at": None,
            "email": "capri123@blueboard.com",
            "vip": False,
            "account_company_name": "Blueboard Client",
            "account_company_id": 18,
            "employee_id": 38728,
            "latest_login": None,
            "active_role": "employee",
            "programs": [],
            "active_managers": [],
            "birthday": thirty_five_years_ago,
            "hired_on": one_year_ago,
        },
        # {
        #     "id": 447,
        #     "gid": "cc0f6d19-65f9-4d27-9341-790a0affe8a7",
        #     "first_name": "Ashish",
        #     "last_name": "Bhatnagar",
        #     "deactivated_at": None,
        #     "email": "ashish@eventbrite.com",
        #     "vip": True,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 4,
        #     "latest_login": "2014-07-14T18:06:06.399862Z",
        #     "active_role": "manager",
        #     "programs": [{"id": 29, "name": "Eventbrite Sales Rewards"}],
        #     "active_managers": [{"id": 6, "program_name": "Eventbrite Sales Rewards"}],
        #     "birthday": thirty_five_years_ago,
        #     "hired_on": just_a_date,
        # },
        # {
        #     "id": 500,
        #     "gid": "23a5054a-8e73-4d66-9d40-6b12ac1f317d",
        #     "first_name": "Tyler",
        #     "last_name": "Chandler",
        #     "deactivated_at": None,
        #     "email": "tchandler@eventbrite.com",
        #     "vip": False,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 39,
        #     "latest_login": "2014-10-13T23:33:50.143431Z",
        #     "active_role": "employee",
        #     "programs": [],
        #     "active_managers": [],
        #     "birthday": just_a_date,
        #     "hired_on": three_years_ago,
        # },
        # {
        #     "id": 501,
        #     "gid": "91022630-83b1-488a-9ada-4ea9c56f06c4",
        #     "first_name": "Ali",
        #     "last_name": "Dockery",
        #     "deactivated_at": None,
        #     "email": "adockery@eventbrite.com",
        #     "vip": False,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 40,
        #     "latest_login": "2014-10-13T23:51:36.976079Z",
        #     "active_role": "employee",
        #     "programs": [],
        #     "active_managers": [],
        #     "birthday": thirty_five_years_ago,
        #     "hired_on": three_years_ago,
        # },
        # {
        #     "id": 502,
        #     "gid": "72975ebf-7532-42f8-9042-f0d40c3e39a0",
        #     "first_name": "Livia",
        #     "last_name": "Marati",
        #     "deactivated_at": None,
        #     "email": "livia@eventbrite.com",
        #     "vip": False,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 38,
        #     "latest_login": "2014-10-13T23:48:20.907779Z",
        #     "active_role": "employee",
        #     "programs": [],
        #     "active_managers": [],
        #     "birthday": just_a_date,
        #     "hired_on": one_year_ago,
        # },
        # {
        #     "id": 503,
        #     "gid": "cb2e4a76-c875-4d20-97b1-369978e6f6ca",
        #     "first_name": "Vanessa",
        #     "last_name": "Vadas",
        #     "deactivated_at": None,
        #     "email": "vadas@eventbrite.com",
        #     "vip": False,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 41,
        #     "latest_login": "2014-10-14T00:06:10.436028Z",
        #     "active_role": "employee",
        #     "programs": [],
        #     "active_managers": [],
        #     "birthday": just_a_date,
        #     "hired_on": ninety_days_ago,
        # },
        # {
        #     "id": 646,
        #     "gid": "b72012fa-8d79-4ae6-a40a-096c73bb4102",
        #     "first_name": "Melissa",
        #     "last_name": "Dempsey",
        #     "deactivated_at": None,
        #     "email": "mdempsey@eventbrite.com",
        #     "vip": False,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 2,
        #     "latest_login": "2015-08-10T17:23:17.453403Z",
        #     "active_role": "employee",
        #     "programs": [],
        #     "active_managers": [],
        #     "birthday": just_a_date,
        #     "hired_on": today,
        # },
        # {
        #     "id": 1095,
        #     "gid": "bddb98d0-d2fa-4214-86fa-6cd61078e342",
        #     "first_name": "Thomas",
        #     "last_name": "St. Clair",
        #     "deactivated_at": None,
        #     "email": "tstclair@eventbrite.com",
        #     "vip": False,
        #     "account_company_name": "Eventbrite",
        #     "account_company_id": 2,
        #     "employee_id": 961,
        #     "latest_login": "2016-05-04T21:25:24.626696Z",
        #     "active_role": "employee",
        #     "programs": [],
        #     "active_managers": [],
        #     "birthday": twenty_years_ago,
        #     "hired_on": just_a_date,
        # },
    ],
    "meta": {
        "total_entries": 7,
        "current_page": 1,
        "next_page": None,
        "previous_page": None,
        "total_count": 7,
    },
}


### Mock POST create rewards response ###

def mock_create_reward_response(company_id):
    return {
        "reward": {
            "id": fake.random_int(min=10000, max=99999),
            # "offering_id": None,
            # "completed_at": None,
            "created_at": fake.date_time_this_year().isoformat(),
            "updated_at": fake.date_time_this_year().isoformat(),
            "code": fake.pystr(),
            "employee_id": fake.random_int(min=10000, max=99999),
            # "day_of_week": None,
            # "how_soon": None,
            # "activity_at": None,
            # "user_notes": None,
            # "deleted_at": None,
            "token": fake.sha1(),
            "feedback_received": fake.boolean(),
            "memo": fake.sentence(),
            "subject": fake.sentence(),
            "company_values_showcased": [
                fake.word(),
                fake.word(),
                fake.word()
            ],
            "company_id": company_id,  # Use the provided id
            "manager_id": fake.random_int(min=10000, max=99999),
            "state": "approved",
            # "redeemed_at": None,
            # "experience_description": None,
            # "reward_type_id": None,
            # "custom_fields": {},
            # "in_discussion": False,
            # "redemption_response_set_access_code": None,
            # "watchlist": False,
            # "denied_at": None,
            # "days_until_sent": None,
            # "days_until_redeemed": None,
            # "days_until_completed": None,
            # "lifetime_in_days": None,
            # "scheduled_at": None,
            # "sent_at": None,
            # "thirty_day_redemption": True,
            # "fully_paid": False,
            # "experience_location": None,
            "approved_at": fake.date_time_this_year().isoformat(),
            # "post_experience_feedback_response_set_access_code": None,
            # "last_approval_reminder_sent_at": None,
            # "fully_paid_date": None,
            # "story_feedback": None,
            # "attachments_url": None,
            # "skip_pre_experience_emails": False,
            # "story_anticipation": None,
            # "employee_location_id": None,
            # "feedback_sent_at": None,
            # "feedback_reminder_sent_at": None,
            # "story_rank": 2,
            # "last_reset_at": None,
            # "deletion_reason": "",
            # "deprecated_deletion_approver": "",
            # "scheduling_at": None,
            # "number_of_people": None,
            # "days_until_activated": None,
            # "activated_at": None,
            # "private_note": "",
            # "flagged": False,
            # "total_expenses": "0.0",
            # "total_customer_reimbursements": "0.0",
            # "custom_priority": None,
            # "selected_location_id": None,
            # "redemption_blocker_survey_response_set_access_code": None,
            # "blocker_reminder_sent_at": None,
            # "calendar_event_id": None,
            # "calendar_invite_sent_at": None,
            # "program_id": 68,
            # "confirmation_email_sent_at": None,
            # "deletion_requested_at": None,
            # "deletion_approver_id": None,
            # "withdrawal_accounting_entity_id": 36853,
            # "place_id": None,
            # "provider_id": None,
            # "skip_blocker_reminder": False,
            # "accepted_legal_liability": None,
            # "skip_post_experience_emails": False,
            # "calendly_call_at": None,
            # "story_internal_note": None,
            # "scheduling_activated": True,
            # "employee_account_id": 30561,
            # "send_as_company": False,
            # "parent_id": None,
            # "accounting_combined": False,
            # "activity_at_time_zone": None,
            # "gid": "b882d7d9-2b48-4bb0-ac8f-00be2815f565",
            # "days_until_scheduled": None,
            # "gif_url": None,
            # "story_images_url": None
        }
    }