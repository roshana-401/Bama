from pydantic_settings import BaseSettings
from typing import Optional

class Setting(BaseSettings):
    account_password:str
    account_username:str
    cluster_name:str
    
    class Config:
        env_file=".env"

    
setting=Setting()