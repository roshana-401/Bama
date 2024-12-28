from pydantic_settings import BaseSettings
from typing import Optional

class Setting(BaseSettings):
    database_hostname:str
    database_dialect:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    database_name_user:str
    class Config:
        env_file=".env"

    
setting=Setting()