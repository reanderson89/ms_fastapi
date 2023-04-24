from sqlmodel import create_engine
from app.configs import db_config

# create the database url using values from db_config
DATABASE_URL = f'mysql+pymysql://{db_config.USER}:{db_config.PASSWD}@{db_config.HOST}:{db_config.PORT}/{db_config.DB}'
engine = create_engine(DATABASE_URL, echo=True)#, connect_args=connect_args)