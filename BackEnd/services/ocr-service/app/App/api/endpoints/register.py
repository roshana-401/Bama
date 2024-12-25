from fastapi import status,Depends,APIRouter
from typing import Annotated
from App.Service.register_service import RegisterService

from App.domain.schemas.user_schema import (
    CreateUser,
    RegisterStepOne,
    RegisterStepTwo,
    VerifyOTPSchema,
    RegisterStepThree,
    UserRegister
)

router=APIRouter(
    tags=["Register"],
    prefix='/user/Sign'
)

@router.post("/SendVerifyMessage",response_model=RegisterStepOne,status_code=status.HTTP_200_OK)

async def registerUser(user:CreateUser,RegisterService:Annotated[RegisterService,Depends()]):
    return await RegisterService.send_OTP(user) 


@router.post("/VerifyMessage",response_model=RegisterStepTwo,status_code=status.HTTP_200_OK)

async def registerUser(user:VerifyOTPSchema,RegisterService:Annotated[RegisterService,Depends()]):
    return await RegisterService.verify_user(user)


@router.post("/Register",response_model=RegisterStepThree,status_code=status.HTTP_201_CREATED)

async def registerUser(user:UserRegister,RegisterService:Annotated[RegisterService,Depends()]):
    return await RegisterService.create_user(user)
        

@router.post("/ResendToken",response_model=RegisterStepTwo,status_code=status.HTTP_200_OK)

async def registerUser(user:CreateUser,RegisterService:Annotated[RegisterService,Depends()]):
    return await RegisterService.resend_otp(user)
     

