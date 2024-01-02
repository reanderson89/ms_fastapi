# from alembic import context
# from burp.models.base_models import Base
# from app.configs.database_configs import db_config

from burp.models.reward import RewardModelDB # noqa: F401
from burp.models.award import AwardModelDB # noqa: F401
from burp.models.client import ClientModelDB # noqa: F401
from burp.models.client_user import ClientUserModelDB # noqa: F401
from burp.models.client_award import ClientAwardModelDB # noqa: F401
from burp.models.client_budget import ClientBudgetModelDB # noqa: F401
from burp.models.message import MessageModelDB # noqa: F401
from burp.models.program_admin import AdminModelDB # noqa: F401
from burp.models.program_award import ProgramAwardModelDB # noqa: F401
from burp.models.program_event import ProgramEventModelDB # noqa: F401
from burp.models.program_rule import ProgramRuleModelDB # noqa: F401
from burp.models.program import ProgramModelDB # noqa: F401
from burp.models.segment_award import SegmentAwardModelDB # noqa: F401
from burp.models.segment_design import SegmentDesignModelDB # noqa: F401
from burp.models.segment_rule import SegmentRuleModelDB # noqa: F401
from burp.models.segment import SegmentModelDB # noqa: F401
from burp.models.base_models import Base # noqa: F401

# # this is the Alembic Config object, which provides
# # access to the values within the .ini file in use.
# config = context.config

# config.set_main_option("sqlalchemy.url",db_config.DATABASE_URL)

# target_metadata = Base.metadata  #find and replace target_metadata with Base.metadata
