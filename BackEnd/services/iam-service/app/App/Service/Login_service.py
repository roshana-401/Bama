from typing import Annotated
from fastapi import Depends, HTTPException, status

from App.domain.schemas.user_schema import (
     LoginUser,
     GetPhoneNumber,
     LoginResponse
)
from App.Service.auth_service.auth_service import AuthService
from App.Service.auth_service.hash_service import HashService
from App.Service.base_service import BaseService
from App.Service.user_service import UserService
from App.domain.models.user_status import UserStatus


class LoginService(BaseService):
    def __init__(
        self,
        user_service: Annotated[UserService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        hash_service: Annotated[HashService, Depends()],
    ) -> None:
        super().__init__()

        self.user_service = user_service
        self.auth_service = auth_service
        self.hash_service = hash_service

    async def LoginUser(self,detail:LoginUser):
        
        if not await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=detail.phone_number)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="کاربر با این شماره تلفن یافت نشد. لطفاً برای ادامه ثبت‌ نام کنید")
        
        user=await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=detail.phone_number))
        
        if user.status!=UserStatus.active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="کاربر با این شماره تلفن یافت نشد. لطفاً برای ادامه ثبت‌ نام کنید")
        
        if not self.hash_service.verifyPassword(detail.password,user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="شماره تلفن یا رمز عبور نادرست است")
        
        token=self.auth_service.create_token({"user_id":str(user.user_id),"role_id":user.role_id,"state":user.status})            
        
        return LoginResponse(message="عملیات با موفقیت انجام شد.",Token=token)
