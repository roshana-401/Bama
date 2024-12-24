from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from .hash_service import HashService
from ..user_service import UserService
from fastapi import status,HTTPException,Depends
from jwt.exceptions import InvalidTokenError
from ..base_service import BaseService
from App.domain.schemas.token_schema import TokenData


class AuthService(BaseService):

    def __init__(
        self,
        hash_service: Annotated[HashService, Depends()],
        user_service: Annotated[UserService, Depends()],
    ) -> None:
        super().__init__()
        self.user_service = user_service
        self.hash_service = hash_service
        
    def create_token(self,data:dict):
        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.config.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt=jwt.encode(to_encode,self.config.secret_key,algorithm=self.config.algorithm)
        return encoded_jwt
        
        
    async def verify_access_token(self,token:str,credentials_exception):
        try:
            payload=jwt.decode(token,self.config.secret_key,algorithms=self.config.algorithm)
            id=payload.get("user_id")
            id=str(id)
            
            if id is None:
                raise credentials_exception
            
            user=await self.user_service.get_user(id)            
        except InvalidTokenError:
            raise credentials_exception
        return user

    def get_current_user(self,token:str):
        credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="شما اهراز هویت نیستید ",
                                            headers={"WWW-Authenticate":"Bearer"})
        return self.verify_access_token(token,credentials_exception)
        