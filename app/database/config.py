import os
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.configs import db_config

# create the database url using values from db_config
DATABASE_URL = f"mysql+pymysql://{db_config.USER}:{db_config.PASSWD}@{db_config.HOST}:{db_config.PORT}/{db_config.DB}"

echo_sql_output: bool = os.environ.get("ENV", "local").lower() == "local"
engine = create_engine(DATABASE_URL, echo=echo_sql_output)


async def get_session():
    with sessionmaker(engine) as session:
        yield session
