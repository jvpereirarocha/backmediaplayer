from dataclasses import dataclass
from os import getenv

@dataclass
class EnvConfigBase:
    DB_URI: str


@dataclass
class ProdConfig(EnvConfigBase):
    DB_URI: str = getenv("DATABASE_URI")


@dataclass
class DevConfig(EnvConfigBase):
    DB_URI: str = getenv("DATABASE_URI")

envs = {
    "production": ProdConfig(),
    "development": DevConfig()
}