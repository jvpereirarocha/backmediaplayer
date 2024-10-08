from dataclasses import dataclass
from os import getenv

@dataclass
class EnvConfigBase:
    DB_URI: str
    SECRET_KEY: str


@dataclass
class ProdConfig(EnvConfigBase):
    DB_URI: str = getenv("DATABASE_URI")
    SECRET_KEY: str = getenv("SECRET_KEY")


@dataclass
class DevConfig(EnvConfigBase):
    DB_URI: str = getenv("DATABASE_URI")
    SECRET_KEY: str = getenv("SECRET_KEY")


envs = {
    "production": ProdConfig(),
    "development": DevConfig()
}