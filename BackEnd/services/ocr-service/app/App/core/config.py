from pydantic_settings import BaseSettings
from typing import Optional

class Setting(BaseSettings):
    database_hostname:str
    database_dialect:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    redis_url:str
    otp_expire_time:str
    access_token_expire_minutes:int
    
    class Config:
        env_file=".env"

    
setting=Setting()