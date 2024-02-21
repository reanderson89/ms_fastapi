import os

from dataclasses import dataclass

env = os.environ.get("ENV", "local")

@dataclass
class BaseDB:
    HOST: str
    USER: str
    PASSWD: str
    PORT: int
    DB: str


@dataclass
class LocalDB(BaseDB):
    # these env vars are coming from docker-compose.yml
    HOST: str = os.environ.get("POSTGRES_HOSTNAME", "localhost")
    PORT: int = os.environ.get("POSTGRES_PORT", 5433)
    USER: str = os.environ.get("POSTGRES_USER", "root")
    PASSWD: str = os.environ.get("POSTGRES_PASSWORD", "password")
    DB: str = os.environ.get("POSTGRES_DB", "blueboard_milestones")


@dataclass
class DevDB(BaseDB):
    # these env vars are coming from docker-compose.yml
    HOST: str = os.environ.get("POSTGRES_HOSTNAME", "0.0.0.0")
    PORT: int = os.environ.get("POSTGRES_PORT", 5432)
    USER: str = os.environ.get("POSTGRES_USER", "root")
    PASSWD: str = os.environ.get("POSTGRES_PASSWORD", "password")
    DB: str = os.environ.get("POSTGRES_DB", "blueboard_milestones")


@dataclass
class StagingDB(BaseDB):
    # these env vars are coming from docker-compose.yml
    HOST: str =  os.environ.get("POSTGRES_HOSTNAME", "localhost")
    PORT: int = os.environ.get("POSTGRES_PORT", 5432)
    USER: str = os.environ.get("POSTGRES_USER", "root")
    PASSWD: str = os.environ.get("POSTGRES_PASSWORD", "password")
    DB: str = os.environ.get("POSTGRES_DB", "blueboard_milestones")


@dataclass
class ProdDB(BaseDB):
    # these env vars are coming from docker-compose.yml
    HOST: str =  os.environ.get("POSTGRES_HOSTNAME", "localhost")
    PORT: int = os.environ.get("POSTGRES_PORT", 5432)
    USER: str = os.environ.get("POSTGRES_USER", "root")
    PASSWD: str = os.environ.get("POSTGRES_PASSWORD", "password")
    DB: str = os.environ.get("POSTGRES_DB", "blueboard_milestones")


configs = {
    "local":LocalDB(),
    "dev":DevDB(),
    "staging":StagingDB(),
    "prod":ProdDB()
}

if env == "dev":
    db_config = configs[env]
    dev_obj = " ".join(map(str, db_config.__dict__.values()))
    print(dev_obj)

db_config = configs[env]
