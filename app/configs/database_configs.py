import os

from dataclasses import dataclass, field

env = os.environ.get('ENV', 'local')

@dataclass
class BaseDB:
	HOST: str
	USER: str
	PASSWD: str
	DB: str
	# SERVER: str
	# FRONTEND: str
	# S3: dict = field(default_factory = lambda:{})

@dataclass
class LocalDB(BaseDB):
	HOST: str = 'localhost'
	PORT: int = 32776
	USER: str = 'root'
	PASSWD: str = 'password'
	DB: str = 'blueboard_milestones'
	#SERVER: str = 'milestone.blueboard.app'
	#FRONTEND: str = 'milestone.blueboard.app'
	# S3: dict = field(default_factory= lambda:{
	# 	'keys': {
	# 			'S3AccessKey' : '',
	# 			'S3SecretKey' : ''
	# 		},
	# 	'media': 'local-media-blueboard-app'
	# 	})

@dataclass
class StagingDB(BaseDB):
	HOST: str = '10.100.1.22'
	USER: str = 'USERNAME'
	PASSWD: str = 'PASSWORD'
	DB: str = 'milestone_staging'
	SERVER: str = 'milestone.blueboard.app'
	FRONTEND: str = 'milestone.blueboard.app'
	S3: dict = field(default_factory= lambda:{
		'keys': {
				'S3AccessKey' : '',
				'S3SecretKey' : ''
			},
		'media': 'staging-media-blueboard-app'
		})

@dataclass
class ProdDB(BaseDB):
	HOST: str = '10.100.1.21'
	USER: str = 'USERNAME'
	PASSWD: str = 'PASSWORD'
	DB: str = 'milestone_prod'
	SERVER: str = 'milestone.blueboard.app'
	FRONTEND: str = 'milestone.blueboard.app'
	S3: dict = field(default_factory= lambda:{
		'keys': {
				'S3AccessKey' : '',
				'S3SecretKey' : ''
			},
		'media': 'media-blueboard-app'
		})

configs = {
	'local':LocalDB(),
	'staging':StagingDB(),
	'prod':ProdDB()
}

db_config = configs[env]