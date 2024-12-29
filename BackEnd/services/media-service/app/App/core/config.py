from pydantic_settings import BaseSettings
from typing import Optional

class Setting(BaseSettings):
    DATABASE_URL: str
    DATABASE_NAME: str
    DATABASE_HOSTNAME:str
    DATABASE_DIALECT:str
    DATABASE_PORT:str
    DATABASE_PASSWORD:str
    DATABASE_USERNAME:str
    DATABASE_NAME_USER:str
    class Config:
        env_file=".env"

    
setting=Setting()