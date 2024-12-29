from typing import Annotated
from fastapi import Depends, HTTPException, status
from uuid import UUID
from App.domain.schemas.user_schema import (
     LoginUserSchema,
     GetPhoneNumber,
     LoginResponse,
     UpdateUser,
     massage,
     VerifyOTPSchema,
     UserUpdatePhoneNumber,
     updatePassword,
     GetPassword
     
)
from App.Service.auth_service.auth_service import AuthService
from App.Service.auth_service.hash_service import HashService
from App.Service.base_service import BaseService
from App.Service.user_service import UserService
from App.Service.auth_service.otp_service import OTPService
from App.domain.models.user_status import UserStatus
from App.infranstructure.repositories.user_repository import UserRepository

class UpdateService(BaseService):
    def __init__(
        self,
        user_service: Annotated[UserService, Depends()],
        auth_service: Annotated[AuthService, Depends()],
        hash_service: Annotated[HashService, Depends()],
        otp_service: Annotated[OTPService, Depends()],
        user_repository:Annotated[UserRepository,Depends()]        
    ) -> None:
        super().__init__()

        self.user_service = user_service
        self.auth_service = auth_service
        self.hash_service = hash_service
        self.otp_service = otp_service
        self.user_repository=user_repository

    async def UpdatePhoneNumberStepOne(self,detail:GetPhoneNumber):
        
        user=await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=detail.phone_number))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=".کاربر با این شماره تلفن یافت نشد")
        
        if user.status!=UserStatus.active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="شماره تلفن وارد شده صحیح نیست. لطفاً دوباره امتحان کنید")
        phone=detail.phone_number+"updated"
        self.otp_service.send_otp(phone)    
        return massage(massage="لطفا  کد تایید ارسالی و شماره تلفن جدید را وارد کنید")
        
    async def UpdatePhoneNumberStepTwo(self, verify_user: UserUpdatePhoneNumber):
        
        user=await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=verify_user.pass_phone_number))
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=".کاربر با این شماره تلفن یافت نشد")
        
        if user.status!=UserStatus.active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="شماره تلفن وارد شده صحیح نیست. لطفاً دوباره امتحان کنید")

        
        is_exist_phoneNumber = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=verify_user.phone_number))

        if is_exist_phoneNumber:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="کاربری با این شماره تلفن در سامانه موجود است")
        
        phone=verify_user.pass_phone_number+"updated"
        if not self.otp_service.verify_otp(phone, verify_user.OTP):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" شماره تلفن یا کد تایید نادرست است لطفا مقادیر را با دقت وارد کنید")
        
        phone=verify_user.phone_number+"updated"
        self.otp_service.send_otp(phone)    
        return massage(massage="لطفا کد تایید ارسالی به شماره تلفن جدید را وارد کنید")
    
    async def UpdatePhoneNumberStepThree(self, verify_user: VerifyOTPSchema,user_id:UUID):
        phone=verify_user.phone_number+"updated"
        if not self.otp_service.verify_otp(phone, verify_user.OTP):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" شماره تلفن یا کد تایید نادرست است لطفا مقادیر را با دقت وارد کنید")

        self.user_repository.update_PhoneNumber_user(user_id=user_id,NewDetail=UpdateUser(phone_number=verify_user.phone_number))
        return massage(massage="شماره تلفن با موفقیت بروزرسانی شد")
    
    async def resend_otp_update_phone_number_step_two(self,phoneNumber:GetPhoneNumber):
    
        exist_user = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=phoneNumber.phone_number))
        if phoneNumber.phone_number!=exist_user.phone_number:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="شماره تلفن وارد شده صحیح نیست. لطفاً دوباره امتحان کنید")
        
        
        phone=phoneNumber.phone_number+"updated"
        if self.otp_service.check_exist(phone):
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="کد تایید معتبر است و هنوز منقضی نشده است")

        self.otp_service.send_otp(phone)
        return massage(massage="لطفا  کد تایید را وارد نمایید")
    
    async def resend_otp_update_phone_number_step_three(self,phoneNumber:GetPhoneNumber,user_id:UUID):
        
        exist_user = await self.user_service.get_user(user_id=user_id)
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=".کاربر با این شماره تلفن یافت نشد")
        
        exist_user = await self.user_service.get_user_with_phone_number(GetPhoneNumber(phone_number=phoneNumber.phone_number))
        if exist_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="کاربری با این شماره تلفن در سامانه موجود است")

        
        phone=phoneNumber.phone_number+"updated"
        if self.otp_service.check_exist(phone):
            raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="کد تایید معتبر است و هنوز منقضی نشده است")

        self.otp_service.send_otp(phone)
        return massage(massage="لطفا  کد تایید را وارد نمایید")
    
    async def update_password(self,info:updatePassword,user_id:UUID):
        
        exist_user = await self.user_service.get_user(user_id=user_id)
        if not exist_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=".کاربر یافت نشد")
        
        if not self.hash_service.verifyPassword(info.pass_password,exist_user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="   رمز عبور نادرست است")
        
        password=self.hash_service.hash(info.password)
        self.user_repository.update_Password_user(exist_user.user_id,password)
        
        return massage(massage="رمز عبور با موفقیت تغییر کرد")

