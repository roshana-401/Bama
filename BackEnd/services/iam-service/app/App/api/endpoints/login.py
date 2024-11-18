from fastapi import status,Depends,APIRouter
from sqlalchemy.orm import Session
from typing import Annotated
from App.Service.Login_service import LoginService

from App.domain.schemas.user_schema import (
    LoginUser,
    LoginResponse
)

router=APIRouter(
    tags=["Login"],
    prefix='/user'
)

@router.post("/Login",response_model=LoginResponse,status_code=status.HTTP_200_OK)

async def LoginUser(user:LoginUser,LoginService:Annotated[LoginService,Depends()]):
    return await LoginService.LoginUser(user) 
