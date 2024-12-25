from fastapi import status,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from App.Service.Login_service import LoginService

from App.domain.schemas.user_schema import (
    LoginUserSchema,
    LoginResponse
)

router=APIRouter(
    tags=["Login"],
    prefix='/user'
)

@router.post("/Login",response_model=LoginResponse,status_code=status.HTTP_200_OK)

async def LoginUser(user:Annotated[OAuth2PasswordRequestForm, Depends()],LoginService:Annotated[LoginService,Depends()]):
    print(user.password)
    print(user.username)
    return await LoginService.LoginUser(LoginUserSchema(phone_number=user.username,password=user.password)) 
