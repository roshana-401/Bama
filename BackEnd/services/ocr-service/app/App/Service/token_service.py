from typing import Annotated
from fastapi import Depends

from App.Service.auth_service.auth_service import AuthService
from App.Service.auth_service.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/user/Login")

async def verify_token(token:str=Depends(oauth2_scheme),auth_service: AuthService = Depends()):
        user=await auth_service.get_current_user(token)

        return user
