import os

from dataclasses import dataclass, field

env = os.environ.get('ENV', 'local')

@dataclass
class BaseDB:
	HOST: str
	USER: str
	PASSWD: str
	PORT: str # int?
	DB: str

@dataclass
class LocalDB(BaseDB):
	# these env vars are coming from docker-compose.yml
	HOST: str =  os.environ.get('MYSQL_HOSTNAME', '127.0.0.1')
	PORT: int = os.environ.get('MYSQL_PORT', '3306')
	USER: str = os.environ.get('MYSQL_USER', 'milestones')
	PASSWD: str = os.environ.get('MYSQL_PASSWORD', 'password')
	DB: str = os.environ.get('MYSQL_DATABASE', 'milestones')

@dataclass
class StagingDB(BaseDB):
	HOST: str = '10.100.1.22'
	PORT: str = '3306'
	USER: str = 'USERNAME'
	PASSWD: str = 'PASSWORD'
	DB: str = 'milestone_staging'

@dataclass
class ProdDB(BaseDB):
	HOST: str = '10.100.1.21'
	PORT: str = '3306'
	USER: str = 'USERNAME'
	PASSWD: str = 'PASSWORD'
	DB: str = 'milestone_prod'

configs = {
	'local':LocalDB(),
	'staging':StagingDB(),
	'prod':ProdDB()
}

db_config = configs[env]