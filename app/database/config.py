from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from app.configs import db_config

# create the database url using values from db_config
DATABASE_URL = f"mysql+pymysql://{db_config.USER}:{db_config.PASSWD}@{db_config.HOST}:{db_config.PORT}/{db_config.DB}"
engine = create_engine(DATABASE_URL, echo=True)

async def get_session():
    with sessionmaker(engine) as session:
        yield session
