from typing import Optional 
from functools import lru_cache
from pydantic import BaseSettings
from dotenv import load_dotenv
import os
# from pydantic_settings import BaseSettings # breaking change in pydantic 2, see https://docs.pydantic.dev/2.7/migration/#basesettings-has-moved-to-pydantic-settings 

load_dotenv()
class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    class Config:
        env_file: str = ".env"

class GlobalConfig(BaseConfig):
    DATABASE_URL: Optional[str] = None # default values
    DB_FORCE_ROLL_BACK: bool = False

class DevConfig(GlobalConfig):
    class Config:
        env_prefix: str = "DEV_" # prefix all env variables with "DEV_"

class ProdConfig(GlobalConfig):
    class Config:
        env_prefix: str = "PROD_"

class TestConfig(GlobalConfig):
    DATABASE_URL = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK = True

    class Config:
        env_prefix: str = "TEST_"

@lru_cache 
def get_config(env_state: str):
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    return configs[env_state]()

config = get_config(os.getenv('ENV_STATE')) #BaseConfig().ENV_STATE)
# allows us to get proper config based on what stage of dev you're in

