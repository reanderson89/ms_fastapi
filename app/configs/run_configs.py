import multiprocessing
import os

from dataclasses import dataclass

env = os.environ.get('ENV', 'local')

#https://www.uvicorn.org/deployment/
#server settings options

@dataclass(repr=False)
class BaseConfig:
	log_level: str = 'info'
	reload: bool = True
	use_colors: bool = True

@dataclass
class LocalConfig(BaseConfig):
	host: str = "127.0.0.1"
	port: int = 8310
	log_level: str = 'debug'

@dataclass
class StagingConfig(BaseConfig):
	host: str = "staging.milestones.blueboard.com"
	#workers: int = multiprocessing.cpu_count()
	log_level: str = 'debug'

@dataclass
class ProdConfig(BaseConfig):
	host: str = "milestones.blueboard.com"
	#workers: int = multiprocessing.cpu_count()
	log_level: str = 'critical'

configs = {
	'local' : LocalConfig(),
	'staging' : StagingConfig(),
	'prod' : ProdConfig()
}

run_config = configs[env]
