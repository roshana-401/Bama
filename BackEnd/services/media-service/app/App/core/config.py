from pydantic_settings import BaseSettings
from typing import Optional

class Setting(BaseSettings):
    DATABASE_URL: str
    DATABASE_NAME: str
    
    class Config:
        env_file=".env"

    
setting=Setting()