from passlib.context import CryptContext
from ..base_service import BaseService


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


class HashService(BaseService):
    def __init__(self) -> None:
        super().__init__() 
        
    @staticmethod
    def hash(password:str):
        hashed_pass=pwd_context.hash(password)
        return hashed_pass

    @staticmethod
    def verifyPassword(plain_password:str,hashed_password:str):
        return pwd_context.verify(plain_password,hashed_password)