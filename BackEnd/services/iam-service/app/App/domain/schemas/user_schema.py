from pydantic import BaseModel,EmailStr,conint,Field
from datetime import datetime
from uuid import UUID



class GetPassword(BaseModel):
    password: str = Field(..., min_length=8, max_length=20)

class massage(BaseModel):
    massage:str
class GetPhoneNumber(BaseModel):
    phone_number:str = Field(..., pattern=r"^09[0-9]{9}$")

class CreateUser(GetPhoneNumber):
    pass

class CreateUserStepThree(GetPhoneNumber,GetPassword):
    pass

class UpdateUser(CreateUser):
    pass


class UpdateStateUser(BaseModel):
    state:str
    
class UpdatePasswordUser(GetPassword,GetPhoneNumber):
    pass    

class UserRegister(GetPhoneNumber,GetPassword):
    pass


class RegisterStepOne(BaseModel):
    message:str
    
class RegisterStepTwo(RegisterStepOne):
    pass

class VerifyOTPSchema(CreateUser):
    OTP: str
    
class RegisterStepThree(RegisterStepOne):
    Token: str
    
class LoginUserSchema(GetPassword,GetPhoneNumber):
    pass

class LoginResponse(RegisterStepThree):
    pass

class UserSchema(GetPhoneNumber):
    user_id:UUID
    status:str
    date_update_Profile:datetime
    date_register:datetime
    role_id:int
    


class user_info(BaseModel):
    user_id:UUID
    date_register:str
    date_update_Profile:str
    status:str
    role:str
class user_list(GetPhoneNumber,user_info):
    pass
    
class UserUpdatePhoneNumber(VerifyOTPSchema):
    pass_phone_number:str= Field(..., pattern=r"^09[0-9]{9}$")
    pass
    
class updatePassword(GetPassword):
    pass_password:str= Field(..., min_length=8, max_length=20)