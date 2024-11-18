from typing import Annotated
from fastapi import Depends, HTTPException, status

from App.domain.schemas.user_schema import (
    CreateUser,
    RegisterStepOne,
    RegisterStepTwo,
    VerifyOTPSchema,
    RegisterStepThree,
    GetPhoneNumber,
    UserRegister,
    CreateUserStepThree,
    GetPassword
)
from App.Service.auth_service.auth_service import AuthService
from App.Service.base_service import BaseService
from App.domain.models.user_status import UserStatus
from App.Service.auth_service.otp_service import OTPService
from App.Service.user_service import UserService


class RegisterService(BaseService):
    def __init__(
        self,
        user_service: Annotated[UserService, Depends()],
        otp_service: Annotated[OTPService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
    ) -> None:
        super().__init__()

        self.user_service = user_service
        self.otp_service = otp_service
        self.auth_service = auth_service

    async def send_OTP(self, user: CreateUser):
        
        is_exist_phoneNumber = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=user.phone_number))

        if is_exist_phoneNumber:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="کاربری با این شماره تلفن در سامانه موجود است")

        new_user = await self.user_service.create_user_stepOne(user)
        
        self.otp_service.send_otp(new_user.phone_number)

        return RegisterStepOne(message="لطفا  کد تایید را وارد نمایید")

    async def verify_user(self, verify_user: VerifyOTPSchema):
        
        if not self.otp_service.verify_otp(verify_user.phone_number, verify_user.OTP):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" شماره تلفن یا کد تایید نادرست است لطفا مقادیر را با دقت وارد کنید")

        user = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=verify_user.phone_number))

        await self.user_service.update_State_user(user.user_id)

        return RegisterStepTwo(message="تایید انجام شد ")

    async def create_user(self,user:UserRegister):
        
       exist_user = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=user.phone_number))
       
       if not exist_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="کاربر با این شماره تلفن یافت نشد. لطفاً برای ادامه ثبت‌ نام کنید")
        
       
       if exist_user.status!=UserStatus.verified:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="شماره تلفن وارد شده صحیح نیست. لطفاً دوباره امتحان کنید")
        
       user=await self.user_service.update_user_RegisterStepThree(exist_user.user_id,CreateUserStepThree(password=user.password,phone_number=user.phone_number))
       token=self.auth_service.create_token({"user_id":str(user.user_id),"role_id":user.role_id,"state":user.status})
       
       return RegisterStepThree(message="ثبت نام با موفقیت انجام شد",Token=token)
   
    async def resend_otp(self,otp:CreateUser):
        exist_user = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=otp.phone_number))
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="شماره تلفن وارد شده صحیح نیست. لطفاً دوباره امتحان کنید")

        if exist_user.status==UserStatus.active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="کاربری با این شماره تلفن در سامانه موجود است")

        if self.otp_service.check_exist(otp.phone_number):
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="کد تایید معتبر است و هنوز منقضی نشده است")

        otp = self.otp_service.send_otp(otp.phone_number)

        return RegisterStepTwo(message="لطفا  کد تایید را وارد نمایید")
